"""
仿真配置模块 —— 定义实验场景参数与全局常量

场景来源：docs/agent_collaboration_design.md §8.1
"""

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class ScenarioConfig:
    """单个实验场景的配置"""

    name: str
    description: str
    num_vehicles: int
    num_rsus: int
    num_tas: int
    threshold_k: int  # 追责门限 k
    simulation_steps: int = 100
    malicious_ratio: float = 0.1  # 恶意车辆比例


# 四个标准实验场景 (S1–S4)
SCENARIOS: Dict[str, ScenarioConfig] = {
    "S1": ScenarioConfig(
        name="S1",
        description="城市路口：单一管理域，中密度交通",
        num_vehicles=200,
        num_rsus=4,
        num_tas=3,
        threshold_k=2,
    ),
    "S2": ScenarioConfig(
        name="S2",
        description="高速公路：单一管理域，高速移动",
        num_vehicles=500,
        num_rsus=10,
        num_tas=3,
        threshold_k=2,
    ),
    "S3": ScenarioConfig(
        name="S3",
        description="跨城通勤：双管理域，车辆跨域频繁",
        num_vehicles=1000,
        num_rsus=20,
        num_tas=6,
        threshold_k=4,
    ),
    "S4": ScenarioConfig(
        name="S4",
        description="大规模城市：单域高密度压力测试",
        num_vehicles=5000,
        num_rsus=50,
        num_tas=5,
        threshold_k=3,
    ),
}


# ---- 信任评估权重 (协议一) ----
TRUST_ALPHA = 0.5  # 本地检测权重
TRUST_BETA = 0.3  # 邻居交叉验证权重
TRUST_GAMMA = 0.2  # 历史信任权重

# ---- 认证阈值 ----
AUTH_FAST_THRESHOLD = 0.8  # trust > 0.8 → 快速认证
AUTH_ENHANCED_THRESHOLD = 0.5  # trust ≤ 0.5 → 增强认证

# ---- 撤销策略 ----
REVOCATION_STRATEGIES = ["VLR", "BloomFilter", "Accumulator", "ZKP"]

# ---- 默认场景 ----
DEFAULT_SCENARIO = "S1"
