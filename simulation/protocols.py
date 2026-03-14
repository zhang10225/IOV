"""
核心协同协议模块 —— 实现 Agent 间的协作流程

协议来源：docs/agent_collaboration_design.md §4

协议一：协同信任评估
协议二：分布式追责决策
协议三：自适应撤销策略协商
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from .agents import BlockchainAgent, RSUAgent, TAAgent, VehicleAgent
from .config import TRUST_ALPHA, TRUST_BETA, TRUST_GAMMA


# ---------------------------------------------------------------------------
# 协议一：协同信任评估
# ---------------------------------------------------------------------------
def collaborative_trust_evaluation(
    rsu: RSUAgent,
    vehicles: List[VehicleAgent],
    alpha: float = TRUST_ALPHA,
    beta: float = TRUST_BETA,
    gamma: float = TRUST_GAMMA,
) -> Dict[str, float]:
    """
    协同信任评估协议。

    步骤:
    1. 每个 Vehicle Agent 运行本地异常检测
    2. RSU Agent 聚合区域内所有 Vehicle Agent 的上报信息
    3. RSU Agent 更新信任分表

    返回: {pseudo_id: trust_score}
    """
    trust_results: Dict[str, float] = {}

    for vehicle in vehicles:
        # 步骤 1: 本地异常检测
        anomaly_score = vehicle.detect_anomaly()
        local_score = 1.0 - anomaly_score  # 异常分越高，信任分越低

        # 步骤 2: 邻居交叉验证（模拟：取其他车辆对该车辆的平均评分）
        neighbor_scores = []
        for other in vehicles:
            if other.pseudo_id != vehicle.pseudo_id:
                # 其他车辆检测该车辆的异常程度（简化模拟）
                if vehicle.is_malicious:
                    neighbor_scores.append(1.0 - other.detect_anomaly() * 0.5)
                else:
                    neighbor_scores.append(0.8 + other.detect_anomaly() * 0.1)
        neighbor_avg = sum(neighbor_scores) / len(neighbor_scores) if neighbor_scores else 0.5

        # 步骤 3: 历史信任（使用当前信任分作为历史）
        history = rsu._trust_table.get(vehicle.pseudo_id, 0.5)

        # 步骤 4: RSU Agent 综合评分
        trust = rsu.update_trust_score(
            vehicle.pseudo_id,
            local_score,
            neighbor_avg,
            history,
            alpha,
            beta,
            gamma,
        )
        trust_results[vehicle.pseudo_id] = trust

    return trust_results


# ---------------------------------------------------------------------------
# 协议二：分布式追责决策
# ---------------------------------------------------------------------------
@dataclass
class TracingResult:
    """追责结果"""

    success: bool
    pseudo_id: str
    real_id: Optional[str] = None
    num_participating_tas: int = 0
    latency_ms: float = 0.0


def distributed_accountability(
    pseudo_id: str,
    evidence: Dict[str, Any],
    ta_agents: List[TAAgent],
    blockchain: BlockchainAgent,
    rsu_agents: List[RSUAgent],
) -> TracingResult:
    """
    分布式追责决策协议。

    步骤:
    1. 追责请求广播至所有 TA Agent
    2. 每个 TA Agent 独立审核证据并计算部分追踪结果
    3. 当至少 k 个 TA Agent 完成后，合成完整追踪结果
    4. 追踪结果提交至 Blockchain Agent，触发撤销
    5. Blockchain Agent 同步撤销列表至所有 RSU Agent
    """
    start_time = time.time()

    if not ta_agents:
        return TracingResult(success=False, pseudo_id=pseudo_id)

    threshold_k = ta_agents[0].threshold_k

    # 步骤 1-2: 收集部分追踪结果
    partial_traces: List[str] = []
    for ta in ta_agents:
        partial = ta.compute_partial_trace(pseudo_id)
        if partial is not None:
            partial_traces.append(partial)

    # 步骤 3: 协同恢复真实身份
    if len(partial_traces) < threshold_k:
        return TracingResult(
            success=False,
            pseudo_id=pseudo_id,
            num_participating_tas=len(partial_traces),
        )

    real_id = ta_agents[0].collaborate_trace(pseudo_id, partial_traces)
    if real_id is None:
        return TracingResult(
            success=False,
            pseudo_id=pseudo_id,
            num_participating_tas=len(partial_traces),
        )

    # 步骤 4: 提交撤销至区块链
    blockchain.execute_revocation(real_id, evidence)
    blockchain.log_event(
        {
            "action": "accountability_trace",
            "pseudo_id": pseudo_id,
            "real_id": real_id,
            "evidence": evidence,
        }
    )

    # 步骤 5: 同步撤销列表
    blockchain.sync_revocation_list(rsu_agents)

    # 同时在 RSU 层面广播假名撤销
    for rsu in rsu_agents:
        rsu.broadcast_revocation(pseudo_id)

    latency = (time.time() - start_time) * 1000  # 转换为毫秒

    return TracingResult(
        success=True,
        pseudo_id=pseudo_id,
        real_id=real_id,
        num_participating_tas=len(partial_traces),
        latency_ms=latency,
    )


# ---------------------------------------------------------------------------
# 协议三：自适应撤销策略协商
# ---------------------------------------------------------------------------
def adaptive_revocation_negotiation(
    rsu_agents: List[RSUAgent],
) -> Dict[str, str]:
    """
    自适应撤销策略协商协议。

    步骤:
    1. 每个 RSU Agent 根据本地状态选择候选撤销策略
    2. 邻近 RSU Agent 交换策略选择
    3. 边界区域的 RSU Agent 协商：采用安全级别较高的策略

    返回: {rsu_id: selected_strategy}
    """
    # 策略安全级别排序（越高越安全）
    security_levels = {
        "VLR": 1,
        "BloomFilter": 2,
        "Accumulator": 3,
        "ZKP": 4,
    }

    # 步骤 1: 各 RSU 独立选择策略
    strategies: Dict[str, str] = {}
    for rsu in rsu_agents:
        strategy = rsu.select_revocation_strategy()
        strategies[rsu.rsu_id] = strategy

    # 步骤 2-3: 邻域协商（取安全级别较高者）
    if len(rsu_agents) > 1:
        # 找到所有 RSU 中安全级别最高的策略
        max_level = max(
            security_levels.get(s, 0) for s in strategies.values()
        )
        # 如果存在高威胁区域，边界 RSU 升级到相同安全级别
        for rsu in rsu_agents:
            current_level = security_levels.get(strategies[rsu.rsu_id], 0)
            if current_level < max_level and rsu._threat_level in ("medium", "high"):
                # 升级到最高安全级别策略
                for strat, level in security_levels.items():
                    if level == max_level:
                        strategies[rsu.rsu_id] = strat
                        rsu.revocation_strategy = strat
                        break

    return strategies
