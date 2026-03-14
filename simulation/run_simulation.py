#!/usr/bin/env python3
"""
IOV 多智能体协同仿真主入口

用法:
    python -m simulation.run_simulation              # 使用默认场景 S1
    python -m simulation.run_simulation --scenario S2 # 指定场景
    python -m simulation.run_simulation --scenario S4 --steps 200

功能:
    1. 初始化四类 Agent（Vehicle、RSU、TA、Blockchain）
    2. 运行协同信任评估协议
    3. 检测恶意车辆并触发分布式追责
    4. 执行自适应撤销策略协商
    5. 输出实验结果统计
"""

from __future__ import annotations

import argparse
import random
import time
from typing import List

from .agents import BlockchainAgent, RSUAgent, TAAgent, VehicleAgent
from .config import SCENARIOS, ScenarioConfig
from .protocols import (
    TracingResult,
    adaptive_revocation_negotiation,
    collaborative_trust_evaluation,
    distributed_accountability,
)


def init_agents(
    cfg: ScenarioConfig,
) -> tuple[List[VehicleAgent], List[RSUAgent], List[TAAgent], BlockchainAgent]:
    """根据场景配置初始化所有 Agent"""

    # ---- Blockchain Agent ----
    blockchain = BlockchainAgent()

    # ---- TA Agents ----
    ta_agents: List[TAAgent] = []
    for i in range(cfg.num_tas):
        ta = TAAgent(
            ta_id=f"TA-{i}",
            threshold_k=cfg.threshold_k,
            total_n=cfg.num_tas,
        )
        ta_agents.append(ta)

    # ---- RSU Agents ----
    rsu_agents: List[RSUAgent] = []
    for i in range(cfg.num_rsus):
        rsu = RSUAgent(rsu_id=f"RSU-{i}", region_id=f"region-{i // 5}")
        # 随机设置交通态势
        density = random.uniform(0.2, 0.9)
        threat = random.choice(["low", "low", "medium", "high"])
        rsu.set_traffic_conditions(density, threat)
        rsu_agents.append(rsu)

    # ---- Vehicle Agents ----
    num_malicious = int(cfg.num_vehicles * cfg.malicious_ratio)
    vehicles: List[VehicleAgent] = []
    for i in range(cfg.num_vehicles):
        is_mal = i < num_malicious
        v = VehicleAgent(
            vehicle_id=f"V-{i:04d}",
            is_malicious=is_mal,
        )
        vehicles.append(v)

        # 注册到最近的 RSU
        assigned_rsu = rsu_agents[i % cfg.num_rsus]
        assigned_rsu.register_vehicle(v)

        # 将假名→真实 ID 映射注册到所有 TA
        for ta in ta_agents:
            ta.register_identity(v.pseudo_id, v.vehicle_id)

    return vehicles, rsu_agents, ta_agents, blockchain


def run_simulation(cfg: ScenarioConfig) -> dict:
    """运行完整仿真流程"""

    print(f"\n{'='*60}")
    print(f"  场景: {cfg.name} — {cfg.description}")
    print(f"  车辆: {cfg.num_vehicles} | RSU: {cfg.num_rsus} | TA: {cfg.num_tas} (k={cfg.threshold_k})")
    print(f"  恶意车辆比例: {cfg.malicious_ratio*100:.0f}%")
    print(f"  仿真步数: {cfg.simulation_steps}")
    print(f"{'='*60}\n")

    vehicles, rsu_agents, ta_agents, blockchain = init_agents(cfg)
    total_start = time.time()

    # ---- 统计变量 ----
    trust_eval_times: List[float] = []
    trace_results: List[TracingResult] = []
    detected_malicious = 0
    total_malicious = sum(1 for v in vehicles if v.is_malicious)

    # ---- 仿真循环 ----
    for step in range(cfg.simulation_steps):
        # 每 10 步打印进度
        if (step + 1) % max(1, cfg.simulation_steps // 10) == 0:
            print(f"  [Step {step+1}/{cfg.simulation_steps}]")

        # 选取一个 RSU 及其管辖的车辆子集进行信任评估
        rsu = rsu_agents[step % cfg.num_rsus]
        subset_size = min(20, len(vehicles))
        vehicle_subset = random.sample(vehicles, subset_size)

        # --- 协议一：协同信任评估 ---
        t0 = time.time()
        trust_scores = collaborative_trust_evaluation(rsu, vehicle_subset)
        trust_eval_times.append((time.time() - t0) * 1000)

        # --- 检测低信任车辆并触发追责 ---
        for v in vehicle_subset:
            score = trust_scores.get(v.pseudo_id, 0.5)
            v.trust_score = score

            # 如果信任分低于阈值，触发追责
            if score < 0.4 and v.is_malicious:
                detected_malicious += 1
                evidence = v.report_evidence(v.pseudo_id, score)

                # --- 协议二：分布式追责 ---
                result = distributed_accountability(
                    pseudo_id=v.pseudo_id,
                    evidence=evidence,
                    ta_agents=ta_agents,
                    blockchain=blockchain,
                    rsu_agents=rsu_agents,
                )
                trace_results.append(result)

    # ---- 协议三：自适应撤销策略协商 ----
    strategy_results = adaptive_revocation_negotiation(rsu_agents)

    total_time = (time.time() - total_start) * 1000

    # ---- 输出结果 ----
    successful_traces = [r for r in trace_results if r.success]
    avg_trust_eval = sum(trust_eval_times) / len(trust_eval_times) if trust_eval_times else 0
    avg_trace_latency = (
        sum(r.latency_ms for r in successful_traces) / len(successful_traces)
        if successful_traces
        else 0
    )

    print(f"\n{'='*60}")
    print("  实验结果统计")
    print(f"{'='*60}")
    print(f"  总仿真时间:              {total_time:.1f} ms")
    print(f"  平均信任评估延迟:        {avg_trust_eval:.2f} ms")
    print(f"  恶意车辆检测次数:        {detected_malicious} / {total_malicious} (总恶意车辆)")
    print(f"  追责请求数:              {len(trace_results)}")
    print(f"  追责成功数:              {len(successful_traces)}")
    print(f"  追责成功率:              {len(successful_traces)/len(trace_results)*100:.1f}%" if trace_results else "  追责成功率:              N/A")
    print(f"  平均追责延迟:            {avg_trace_latency:.2f} ms")
    print(f"  区块链撤销数:            {blockchain.revocation_count}")
    print(f"  审计日志条目:            {blockchain.audit_log_size}")
    print()
    print("  RSU 撤销策略分布:")
    strategy_count: dict[str, int] = {}
    for strat in strategy_results.values():
        strategy_count[strat] = strategy_count.get(strat, 0) + 1
    for strat, count in sorted(strategy_count.items()):
        print(f"    {strat}: {count} 个 RSU")
    print(f"{'='*60}\n")

    return {
        "scenario": cfg.name,
        "total_time_ms": total_time,
        "avg_trust_eval_ms": avg_trust_eval,
        "detected_malicious": detected_malicious,
        "total_malicious": total_malicious,
        "trace_requests": len(trace_results),
        "trace_success": len(successful_traces),
        "trace_success_rate": len(successful_traces) / len(trace_results) if trace_results else 0,
        "avg_trace_latency_ms": avg_trace_latency,
        "revocation_count": blockchain.revocation_count,
        "audit_log_size": blockchain.audit_log_size,
        "strategy_distribution": strategy_count,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="IOV 多智能体协同仿真")
    parser.add_argument(
        "--scenario",
        type=str,
        default="S1",
        choices=list(SCENARIOS.keys()),
        help="实验场景 (S1/S2/S3/S4)",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=None,
        help="仿真步数 (覆盖场景默认值)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="随机种子",
    )
    args = parser.parse_args()

    random.seed(args.seed)

    cfg = SCENARIOS[args.scenario]
    if args.steps is not None:
        cfg.simulation_steps = args.steps

    run_simulation(cfg)


if __name__ == "__main__":
    main()
