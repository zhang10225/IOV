"""
多智能体核心模块 —— VehicleAgent / RSUAgent / TAAgent / BlockchainAgent

设计来源：docs/agent_collaboration_design.md §3
"""

from __future__ import annotations

import hashlib
import random
import secrets
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple


# ---------------------------------------------------------------------------
# Vehicle Agent
# ---------------------------------------------------------------------------
@dataclass
class VehicleAgent:
    """车辆层智能体 —— 消息签名、邻居监测和证据上报"""

    vehicle_id: str
    pseudo_id: str = ""
    trust_score: float = 0.5
    is_malicious: bool = False

    # 内部状态
    _neighbors: List[str] = field(default_factory=list)
    _message_log: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.pseudo_id:
            self.pseudo_id = f"pseudo_{secrets.token_hex(4)}"

    # ---- 动作 ----

    def sign_message(self, content: str) -> Dict[str, str]:
        """使用当前假名对消息签名（简化模拟，用 HMAC-SHA256 代替 ECC）"""
        sig = hashlib.sha256(
            f"{self.pseudo_id}:{content}".encode()
        ).hexdigest()
        msg = {
            "sender": self.pseudo_id,
            "content": content,
            "signature": sig,
            "timestamp": str(time.time()),
        }
        self._message_log.append(msg)
        return msg

    def verify_neighbor(self, msg: Dict[str, str]) -> bool:
        """验证邻居消息签名"""
        expected = hashlib.sha256(
            f"{msg['sender']}:{msg['content']}".encode()
        ).hexdigest()
        return expected == msg.get("signature")

    def detect_anomaly(self) -> float:
        """
        本地异常检测（简化模拟）。
        恶意车辆有 70% 概率被检测到异常。
        """
        if self.is_malicious:
            return random.uniform(0.6, 1.0)  # 高异常分
        return random.uniform(0.0, 0.3)  # 低异常分

    def report_evidence(self, target_pseudo_id: str, anomaly_score: float) -> Dict[str, Any]:
        """向 RSU 上报异常证据"""
        return {
            "reporter": self.pseudo_id,
            "target": target_pseudo_id,
            "anomaly_score": anomaly_score,
            "timestamp": time.time(),
        }

    def request_new_pseudonym(self) -> str:
        """请求新假名"""
        self.pseudo_id = f"pseudo_{secrets.token_hex(4)}"
        return self.pseudo_id


# ---------------------------------------------------------------------------
# RSU Agent
# ---------------------------------------------------------------------------
@dataclass
class RSUAgent:
    """边缘层智能体 —— 区域认证、信任管理和自适应撤销"""

    rsu_id: str
    region_id: str = "default"
    revocation_strategy: str = "VLR"

    # 内部状态
    _vehicle_registry: Dict[str, VehicleAgent] = field(default_factory=dict)
    _trust_table: Dict[str, float] = field(default_factory=dict)
    _traffic_density: float = 0.5
    _threat_level: str = "low"
    _revocation_list: Set[str] = field(default_factory=set)

    # ---- 动作 ----

    def register_vehicle(self, vehicle: VehicleAgent) -> None:
        """注册车辆到本区域"""
        self._vehicle_registry[vehicle.pseudo_id] = vehicle
        self._trust_table[vehicle.pseudo_id] = vehicle.trust_score

    def authenticate_vehicle(self, vehicle: VehicleAgent) -> Tuple[bool, str]:
        """
        认证车辆，根据信任分选择认证强度。

        返回: (是否通过, 认证级别)
        """
        trust = self._trust_table.get(vehicle.pseudo_id, 0.5)

        if vehicle.pseudo_id in self._revocation_list:
            return False, "revoked"

        if trust > 0.8:
            return True, "fast"
        elif trust > 0.5:
            return True, "standard"
        else:
            # 增强认证：恶意车辆有概率被拒绝
            if vehicle.is_malicious and random.random() < 0.6:
                return False, "enhanced_rejected"
            return True, "enhanced"

    def update_trust_score(
        self,
        pseudo_id: str,
        local_score: float,
        neighbor_reports: float,
        history_score: float,
        alpha: float = 0.5,
        beta: float = 0.3,
        gamma: float = 0.2,
    ) -> float:
        """
        综合信任评估。

        trust = α × local_score + β × neighbor_reports + γ × history
        """
        trust = alpha * local_score + beta * neighbor_reports + gamma * history_score
        trust = max(0.0, min(1.0, trust))
        self._trust_table[pseudo_id] = trust
        return trust

    def select_revocation_strategy(self) -> str:
        """
        自适应撤销策略选择。

        策略映射:
        - 低密度 + 低威胁 → VLR
        - 高密度 + 低威胁 → BloomFilter
        - 高密度 + 高威胁 → Accumulator
        - 跨域          → ZKP
        """
        if self._traffic_density < 0.5 and self._threat_level == "low":
            self.revocation_strategy = "VLR"
        elif self._traffic_density >= 0.5 and self._threat_level == "low":
            self.revocation_strategy = "BloomFilter"
        elif self._traffic_density >= 0.5 and self._threat_level in ("medium", "high"):
            self.revocation_strategy = "Accumulator"
        else:
            self.revocation_strategy = "ZKP"
        return self.revocation_strategy

    def broadcast_revocation(self, pseudo_id: str) -> None:
        """将车辆加入撤销列表"""
        self._revocation_list.add(pseudo_id)

    def set_traffic_conditions(self, density: float, threat: str) -> None:
        """设置当前交通态势（由仿真控制器调用）"""
        self._traffic_density = density
        self._threat_level = threat


# ---------------------------------------------------------------------------
# TA Agent
# ---------------------------------------------------------------------------
@dataclass
class TAAgent:
    """管理层智能体 —— 协同追责与身份还原（门限秘密共享）"""

    ta_id: str
    threshold_k: int = 2
    total_n: int = 3

    # 内部状态：假名 → 真实 ID 映射（由系统初始化时注入）
    _identity_map: Dict[str, str] = field(default_factory=dict)
    _secret_share: bytes = field(default_factory=lambda: secrets.token_bytes(32))
    _trace_log: List[Dict[str, Any]] = field(default_factory=list)

    def register_identity(self, pseudo_id: str, real_id: str) -> None:
        """注册假名与真实身份映射"""
        self._identity_map[pseudo_id] = real_id

    def compute_partial_trace(self, pseudo_id: str) -> Optional[str]:
        """
        计算部分追踪结果。
        简化模拟：使用 HMAC(secret_share, pseudo_id) 作为部分追踪值。
        """
        if pseudo_id not in self._identity_map:
            return None
        partial = hashlib.sha256(
            self._secret_share + pseudo_id.encode()
        ).hexdigest()[:16]
        return partial

    def collaborate_trace(
        self,
        pseudo_id: str,
        partial_traces: List[str],
    ) -> Optional[str]:
        """
        协同追踪 —— 收集到 k 个部分追踪结果后恢复真实身份。
        简化模拟：直接从映射表中返回真实身份。
        """
        if len(partial_traces) < self.threshold_k:
            return None  # 不够门限
        real_id = self._identity_map.get(pseudo_id)
        if real_id:
            self._trace_log.append(
                {
                    "pseudo_id": pseudo_id,
                    "real_id": real_id,
                    "num_partials": len(partial_traces),
                    "timestamp": time.time(),
                }
            )
        return real_id


# ---------------------------------------------------------------------------
# Blockchain Agent
# ---------------------------------------------------------------------------
@dataclass
class BlockchainAgent:
    """区块链层智能体 —— 执行合约、维护撤销列表"""

    _revocation_list: Set[str] = field(default_factory=set)
    _audit_log: List[Dict[str, Any]] = field(default_factory=list)

    def execute_revocation(self, real_id: str, evidence: Dict[str, Any]) -> bool:
        """执行撤销合约"""
        if real_id in self._revocation_list:
            return False  # 已撤销
        self._revocation_list.add(real_id)
        self._audit_log.append(
            {
                "action": "revocation",
                "real_id": real_id,
                "evidence": evidence,
                "timestamp": time.time(),
            }
        )
        return True

    def query_revocation_status(self, real_id: str) -> bool:
        """查询是否已被撤销"""
        return real_id in self._revocation_list

    def log_event(self, event: Dict[str, Any]) -> None:
        """记录追责事件到审计日志"""
        event["timestamp"] = time.time()
        self._audit_log.append(event)

    def sync_revocation_list(self, rsu_agents: List[RSUAgent]) -> int:
        """
        同步撤销列表至所有 RSU Agent。
        返回同步的 RSU 数量。
        """
        for rsu in rsu_agents:
            for revoked_id in self._revocation_list:
                rsu.broadcast_revocation(revoked_id)
        return len(rsu_agents)

    @property
    def revocation_count(self) -> int:
        return len(self._revocation_list)

    @property
    def audit_log_size(self) -> int:
        return len(self._audit_log)
