"""
多智能体协同仿真——单元测试

覆盖范围：
- Agent 基础功能（签名、验证、认证、追责、撤销）
- 协同协议（信任评估、分布式追责、自适应撤销）
- 端到端仿真流程
"""

import random

import pytest

from simulation.agents import BlockchainAgent, RSUAgent, TAAgent, VehicleAgent
from simulation.config import SCENARIOS
from simulation.protocols import (
    adaptive_revocation_negotiation,
    collaborative_trust_evaluation,
    distributed_accountability,
)
from simulation.run_simulation import init_agents, run_simulation


# ============================================================
# VehicleAgent 测试
# ============================================================
class TestVehicleAgent:
    def test_init_generates_pseudo_id(self):
        v = VehicleAgent(vehicle_id="V-001")
        assert v.pseudo_id.startswith("pseudo_")
        assert len(v.pseudo_id) > 7

    def test_sign_and_verify(self):
        v = VehicleAgent(vehicle_id="V-001")
        msg = v.sign_message("hello")
        assert msg["sender"] == v.pseudo_id
        assert msg["content"] == "hello"
        assert "signature" in msg
        assert v.verify_neighbor(msg) is True

    def test_verify_rejects_tampered(self):
        v = VehicleAgent(vehicle_id="V-001")
        msg = v.sign_message("hello")
        msg["content"] = "tampered"
        assert v.verify_neighbor(msg) is False

    def test_detect_anomaly_malicious(self):
        random.seed(42)
        v = VehicleAgent(vehicle_id="V-001", is_malicious=True)
        scores = [v.detect_anomaly() for _ in range(100)]
        avg = sum(scores) / len(scores)
        # 恶意车辆的平均异常分应较高
        assert avg > 0.5

    def test_detect_anomaly_normal(self):
        random.seed(42)
        v = VehicleAgent(vehicle_id="V-002", is_malicious=False)
        scores = [v.detect_anomaly() for _ in range(100)]
        avg = sum(scores) / len(scores)
        # 正常车辆的平均异常分应较低
        assert avg < 0.3

    def test_report_evidence(self):
        v = VehicleAgent(vehicle_id="V-001")
        evidence = v.report_evidence("target_pseudo", 0.9)
        assert evidence["reporter"] == v.pseudo_id
        assert evidence["target"] == "target_pseudo"
        assert evidence["anomaly_score"] == 0.9

    def test_request_new_pseudonym(self):
        v = VehicleAgent(vehicle_id="V-001")
        old_pseudo = v.pseudo_id
        new_pseudo = v.request_new_pseudonym()
        assert new_pseudo != old_pseudo
        assert v.pseudo_id == new_pseudo


# ============================================================
# RSUAgent 测试
# ============================================================
class TestRSUAgent:
    def test_register_vehicle(self):
        rsu = RSUAgent(rsu_id="RSU-0")
        v = VehicleAgent(vehicle_id="V-001")
        rsu.register_vehicle(v)
        assert v.pseudo_id in rsu._vehicle_registry
        assert v.pseudo_id in rsu._trust_table

    def test_authenticate_fast(self):
        rsu = RSUAgent(rsu_id="RSU-0")
        v = VehicleAgent(vehicle_id="V-001", trust_score=0.9)
        rsu.register_vehicle(v)
        rsu._trust_table[v.pseudo_id] = 0.9
        passed, level = rsu.authenticate_vehicle(v)
        assert passed is True
        assert level == "fast"

    def test_authenticate_revoked(self):
        rsu = RSUAgent(rsu_id="RSU-0")
        v = VehicleAgent(vehicle_id="V-001")
        rsu.register_vehicle(v)
        rsu.broadcast_revocation(v.pseudo_id)
        passed, level = rsu.authenticate_vehicle(v)
        assert passed is False
        assert level == "revoked"

    def test_update_trust_score(self):
        rsu = RSUAgent(rsu_id="RSU-0")
        trust = rsu.update_trust_score("pseudo_abc", 0.8, 0.6, 0.5)
        expected = 0.5 * 0.8 + 0.3 * 0.6 + 0.2 * 0.5  # 0.68
        assert abs(trust - expected) < 1e-6

    def test_select_strategy_low_density_low_threat(self):
        rsu = RSUAgent(rsu_id="RSU-0")
        rsu.set_traffic_conditions(0.3, "low")
        assert rsu.select_revocation_strategy() == "VLR"

    def test_select_strategy_high_density_low_threat(self):
        rsu = RSUAgent(rsu_id="RSU-0")
        rsu.set_traffic_conditions(0.7, "low")
        assert rsu.select_revocation_strategy() == "BloomFilter"

    def test_select_strategy_high_density_high_threat(self):
        rsu = RSUAgent(rsu_id="RSU-0")
        rsu.set_traffic_conditions(0.8, "high")
        assert rsu.select_revocation_strategy() == "Accumulator"


# ============================================================
# TAAgent 测试
# ============================================================
class TestTAAgent:
    def test_register_and_partial_trace(self):
        ta = TAAgent(ta_id="TA-0", threshold_k=2, total_n=3)
        ta.register_identity("pseudo_abc", "V-001")
        partial = ta.compute_partial_trace("pseudo_abc")
        assert partial is not None
        assert len(partial) == 16

    def test_partial_trace_unknown_pseudo(self):
        ta = TAAgent(ta_id="TA-0")
        assert ta.compute_partial_trace("unknown") is None

    def test_collaborate_trace_success(self):
        ta = TAAgent(ta_id="TA-0", threshold_k=2, total_n=3)
        ta.register_identity("pseudo_abc", "V-001")
        real_id = ta.collaborate_trace("pseudo_abc", ["partial1", "partial2"])
        assert real_id == "V-001"
        assert len(ta._trace_log) == 1

    def test_collaborate_trace_insufficient_partials(self):
        ta = TAAgent(ta_id="TA-0", threshold_k=2, total_n=3)
        ta.register_identity("pseudo_abc", "V-001")
        real_id = ta.collaborate_trace("pseudo_abc", ["partial1"])
        assert real_id is None


# ============================================================
# BlockchainAgent 测试
# ============================================================
class TestBlockchainAgent:
    def test_execute_revocation(self):
        bc = BlockchainAgent()
        assert bc.execute_revocation("V-001", {"reason": "malicious"}) is True
        assert bc.revocation_count == 1
        assert bc.query_revocation_status("V-001") is True

    def test_duplicate_revocation(self):
        bc = BlockchainAgent()
        bc.execute_revocation("V-001", {"reason": "malicious"})
        assert bc.execute_revocation("V-001", {"reason": "duplicate"}) is False
        assert bc.revocation_count == 1

    def test_sync_revocation_list(self):
        bc = BlockchainAgent()
        bc.execute_revocation("V-001", {})
        rsu1 = RSUAgent(rsu_id="RSU-0")
        rsu2 = RSUAgent(rsu_id="RSU-1")
        synced = bc.sync_revocation_list([rsu1, rsu2])
        assert synced == 2
        assert "V-001" in rsu1._revocation_list
        assert "V-001" in rsu2._revocation_list

    def test_log_event(self):
        bc = BlockchainAgent()
        bc.log_event({"action": "test"})
        assert bc.audit_log_size == 1


# ============================================================
# 协议测试
# ============================================================
class TestProtocols:
    def test_collaborative_trust_evaluation(self):
        random.seed(42)
        rsu = RSUAgent(rsu_id="RSU-0")
        vehicles = [
            VehicleAgent(vehicle_id=f"V-{i}", is_malicious=(i == 0))
            for i in range(5)
        ]
        for v in vehicles:
            rsu.register_vehicle(v)

        scores = collaborative_trust_evaluation(rsu, vehicles)
        assert len(scores) == 5
        # 恶意车辆的信任分应低于正常车辆的平均值
        malicious_score = scores[vehicles[0].pseudo_id]
        normal_scores = [scores[v.pseudo_id] for v in vehicles[1:]]
        avg_normal = sum(normal_scores) / len(normal_scores)
        assert malicious_score < avg_normal

    def test_distributed_accountability_success(self):
        ta_agents = [
            TAAgent(ta_id=f"TA-{i}", threshold_k=2, total_n=3)
            for i in range(3)
        ]
        for ta in ta_agents:
            ta.register_identity("pseudo_mal", "V-BAD")

        bc = BlockchainAgent()
        rsu_agents = [RSUAgent(rsu_id="RSU-0")]

        result = distributed_accountability(
            pseudo_id="pseudo_mal",
            evidence={"score": 0.1},
            ta_agents=ta_agents,
            blockchain=bc,
            rsu_agents=rsu_agents,
        )
        assert result.success is True
        assert result.real_id == "V-BAD"
        assert bc.query_revocation_status("V-BAD") is True

    def test_distributed_accountability_unknown_pseudo(self):
        ta_agents = [
            TAAgent(ta_id=f"TA-{i}", threshold_k=2, total_n=3)
            for i in range(3)
        ]
        bc = BlockchainAgent()
        result = distributed_accountability(
            pseudo_id="unknown",
            evidence={},
            ta_agents=ta_agents,
            blockchain=bc,
            rsu_agents=[],
        )
        assert result.success is False

    def test_adaptive_revocation_negotiation(self):
        rsu_agents = [
            RSUAgent(rsu_id="RSU-0"),
            RSUAgent(rsu_id="RSU-1"),
        ]
        rsu_agents[0].set_traffic_conditions(0.3, "low")
        rsu_agents[1].set_traffic_conditions(0.8, "high")

        strategies = adaptive_revocation_negotiation(rsu_agents)
        assert "RSU-0" in strategies
        assert "RSU-1" in strategies
        # RSU-1 高密度高威胁应选择 Accumulator
        assert strategies["RSU-1"] == "Accumulator"


# ============================================================
# 端到端仿真测试
# ============================================================
class TestEndToEnd:
    def test_init_agents_s1(self):
        random.seed(42)
        cfg = SCENARIOS["S1"]
        vehicles, rsus, tas, bc = init_agents(cfg)
        assert len(vehicles) == 200
        assert len(rsus) == 4
        assert len(tas) == 3
        assert isinstance(bc, BlockchainAgent)

    def test_run_simulation_s1(self):
        random.seed(42)
        cfg = SCENARIOS["S1"]
        cfg.simulation_steps = 10  # 快速测试
        result = run_simulation(cfg)
        assert result["scenario"] == "S1"
        assert result["total_time_ms"] > 0
        assert "strategy_distribution" in result
