# Agent 加入指南：如何复现与改进实验

> 本文档提供从零开始加入 Agent 协同机制、复现基线实验并逐步改进的完整操作指南。
> 配合 [多智能体协同设计方案](agent_collaboration_design.md) 和 [文献综述](literature_review.md) 阅读效果最佳。

---

## 目录

1. [总体思路](#1-总体思路)
2. [环境准备](#2-环境准备)
3. [快速体验：运行仿真原型](#3-快速体验运行仿真原型)
4. [阶段一：基线复现（无 Agent）](#4-阶段一基线复现无-agent)
5. [阶段二：加入 Agent 协同](#5-阶段二加入-agent-协同)
6. [阶段三：改进实验](#6-阶段三改进实验)
7. [实验结果记录与对比](#7-实验结果记录与对比)
8. [常见问题](#8-常见问题)

---

## 1. 总体思路

加入 Agent 协同机制的核心路线：

```
基线复现（无 Agent）  →  加入 Agent 协同  →  改进与优化
      ↓                      ↓                    ↓
  单一方案验证          多 Agent 协作         消融实验 + 参数调优
  P1–P10 各自独立       车辆/RSU/TA/区块链     对比有无 Agent 的性能差异
                        四类 Agent 协同
```

**三个阶段的关系**：

| 阶段 | 目标 | 输出 |
|------|------|------|
| 基线复现 | 验证单一方案的正确性，获得基线数据 | 各论文核心指标的基准值 |
| 加入 Agent | 将各实体建模为自主 Agent，实现协同协议 | Agent 协同版本的性能数据 |
| 改进实验 | 通过消融实验和参数调优，量化 Agent 协同的增益 | 对比图表、改进方案的定量证据 |

---

## 2. 环境准备

### 2.1 基础环境（必需）

```bash
# 操作系统
Ubuntu 22.04 LTS（推荐）或 macOS 13+

# Python 环境
python3 --version   # 需要 Python 3.8+
pip3 install pytest  # 测试框架

# 克隆项目
git clone https://github.com/zhang10225/IOV.git
cd IOV
```

### 2.2 密码学库（阶段一需要）

```bash
# 方案 A：Charm-Crypto（推荐，Python 密码学原型框架）
pip3 install charm-crypto

# 方案 B：PBC Library（C 语言，高性能）
sudo apt-get install -y libgmp-dev flex bison
git clone https://github.com/blynn/pbc.git
cd pbc && ./setup && ./configure && make && sudo make install
```

### 2.3 Agent 框架（阶段二需要）

```bash
# 方案 A：SPADE（推荐，快速原型验证）
pip3 install spade

# 方案 B：Mesa（大规模 Agent 仿真）
pip3 install mesa

# 方案 C：自定义轻量框架（性能优先）
pip3 install pyzmq grpcio grpcio-tools
```

### 2.4 扩展工具（阶段三按需安装）

```bash
# 区块链
npm install -g hardhat
pip3 install web3

# 联邦学习
pip3 install flwr torch

# 交通仿真
sudo apt-get install sumo sumo-tools  # SUMO 1.18+

# ZKP
npm install -g snarkjs circom
```

### 2.5 Docker 统一环境（可选，推荐）

项目提供了参考 Dockerfile（见 [文献综述 附录 B](literature_review.md)），可直接构建统一环境：

```bash
docker build -t iov-sim .
docker run -it -v $(pwd):/workspace iov-sim bash
```

---

## 3. 快速体验：运行仿真原型

项目已包含一个多 Agent 协同仿真原型（`simulation/` 目录），可直接运行：

```bash
# 在项目根目录下

# 运行默认场景 S1（城市路口，200 车辆，4 RSU，3 TA）
python -m simulation.run_simulation

# 运行更大规模的场景
python -m simulation.run_simulation --scenario S2   # 高速公路 500 车辆
python -m simulation.run_simulation --scenario S4   # 大规模 5000 车辆

# 运行测试验证代码正确性
python -m pytest tests/test_simulation.py -v
```

仿真原型包含四类 Agent 和三项核心协议的简化实现，输出包括：
- 信任评估延迟
- 恶意车辆检测率
- 追责成功率和延迟
- RSU 撤销策略分布

---

## 4. 阶段一：基线复现（无 Agent）

### 4.1 选择论文

根据研究方向选择 1–2 篇论文作为基线（推荐从以下开始）：

| 推荐顺序 | 论文 | 理由 |
|----------|------|------|
| ⭐ 首选 | P1 (ECC 条件隐私认证) | 复现难度最低，核心算法清晰 |
| ⭐ 首选 | P4 (布隆过滤器撤销) | 实现简单，效果直观 |
| 进阶 | P3 (VLR 群签名) | 追责+撤销完整流程 |
| 进阶 | P10 (联邦学习检测) | ML 背景读者推荐 |

### 4.2 复现步骤（以 P1 为例）

```python
# 步骤 1：实现 ECC 签名（使用 Charm-Crypto）
from charm.toolbox.pairinggroup import PairingGroup, ZR, G1

group = PairingGroup('MNT224')  # 或 'BN254'

# 密钥生成
sk = group.random(ZR)
pk = group.random(G1) ** sk

# 签名
def sign(message, sk):
    h = group.hash(message, G1)
    return h ** sk

# 验证
def verify(message, signature, pk):
    h = group.hash(message, G1)
    return group.pair_prod(signature, group.random(G1)) == group.pair_prod(h, pk)
```

```python
# 步骤 2：批量验证
import time

messages = [f"msg_{i}" for i in range(1000)]
signatures = [sign(m, sk) for m in messages]

# 单次验证计时
start = time.time()
for m, s in zip(messages, signatures):
    verify(m, s, pk)
single_time = time.time() - start

# 批量验证计时（随机线性组合）
start = time.time()
# ... 实现批量验证逻辑 ...
batch_time = time.time() - start

print(f"单次验证总时间: {single_time*1000:.1f} ms")
print(f"批量验证总时间: {batch_time*1000:.1f} ms")
print(f"加速比: {single_time/batch_time:.2f}x")
```

```python
# 步骤 3：追踪与撤销
# TA 使用追踪密钥恢复真实身份
def trace(pseudo_signature, tracing_key):
    real_id = decrypt(pseudo_signature.tag, tracing_key)
    return real_id

# 撤销列表检查
revocation_list = set()
def is_revoked(vehicle_id):
    return vehicle_id in revocation_list
```

### 4.3 记录基线数据

创建实验记录表格：

| 指标 | 论文报告值 | 复现值 | 偏差 | 原因分析 |
|------|-----------|--------|------|----------|
| 签名时间 (ms) | 2.3 | ? | | |
| 验证时间 (ms) | 3.1 | ? | | |
| 批量验证加速比 | 5.2x | ? | | |
| 通信开销 (bytes) | 128 | ? | | |
| 追踪恢复时间 (ms) | 1.5 | ? | | |

---

## 5. 阶段二：加入 Agent 协同

### 5.1 核心思路

将阶段一中的单一方案改造为多 Agent 协同版本：

```
改造前（单一方案）:
  车辆 → 签名 → RSU 验证 → TA 追踪 → 撤销列表更新

改造后（Agent 协同）:
  Vehicle Agent → 签名 + 本地异常检测
       ↓
  RSU Agent → 认证 + 信任评估 + 自适应撤销策略
       ↓
  TA Agent ×k → 门限协同追责（MPC）
       ↓
  Blockchain Agent → 撤销合约 + 审计日志
```

### 5.2 使用仿真原型的 Agent 类

项目 `simulation/` 目录已提供四类 Agent 的基础实现，可直接继承和扩展：

```python
from simulation.agents import VehicleAgent, RSUAgent, TAAgent, BlockchainAgent

# 方法 1：直接使用（快速验证）
vehicle = VehicleAgent(vehicle_id="V-001")
msg = vehicle.sign_message("safety_message")

rsu = RSUAgent(rsu_id="RSU-0")
rsu.register_vehicle(vehicle)
passed, level = rsu.authenticate_vehicle(vehicle)

# 方法 2：继承扩展（加入真实密码学）
class EccVehicleAgent(VehicleAgent):
    """使用真实 ECC 签名替换简化签名"""

    def sign_message(self, content: str):
        # 使用 Charm-Crypto 的 ECC 签名
        h = self.group.hash(content, G1)
        sig = h ** self.sk
        return {"sender": self.pseudo_id, "content": content, "signature": sig}
```

### 5.3 实现协同协议

#### 协议一：协同信任评估

```python
from simulation.protocols import collaborative_trust_evaluation

# 直接调用已实现的协议
rsu = RSUAgent(rsu_id="RSU-0")
vehicles = [VehicleAgent(vehicle_id=f"V-{i}") for i in range(50)]
for v in vehicles:
    rsu.register_vehicle(v)

trust_scores = collaborative_trust_evaluation(rsu, vehicles)
# trust_scores = {"pseudo_xxx": 0.82, "pseudo_yyy": 0.35, ...}
```

#### 协议二：分布式追责

```python
from simulation.protocols import distributed_accountability

ta_agents = [TAAgent(ta_id=f"TA-{i}", threshold_k=2, total_n=3) for i in range(3)]
blockchain = BlockchainAgent()

# 注册身份映射
for ta in ta_agents:
    ta.register_identity("pseudo_malicious", "V-BAD-001")

# 触发追责
result = distributed_accountability(
    pseudo_id="pseudo_malicious",
    evidence={"anomaly_score": 0.95, "reports": 5},
    ta_agents=ta_agents,
    blockchain=blockchain,
    rsu_agents=[rsu],
)

print(f"追责成功: {result.success}")
print(f"真实身份: {result.real_id}")
print(f"追责延迟: {result.latency_ms:.2f} ms")
```

#### 协议三：自适应撤销策略

```python
from simulation.protocols import adaptive_revocation_negotiation

rsu_agents = [RSUAgent(rsu_id=f"RSU-{i}") for i in range(5)]
rsu_agents[0].set_traffic_conditions(0.3, "low")    # VLR
rsu_agents[1].set_traffic_conditions(0.7, "low")    # BloomFilter
rsu_agents[2].set_traffic_conditions(0.8, "high")   # Accumulator
rsu_agents[3].set_traffic_conditions(0.5, "medium") # Accumulator
rsu_agents[4].set_traffic_conditions(0.2, "low")    # VLR

strategies = adaptive_revocation_negotiation(rsu_agents)
# {"RSU-0": "VLR", "RSU-1": "BloomFilter", "RSU-2": "Accumulator", ...}
```

### 5.4 集成到 SPADE Agent 框架（进阶）

```python
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class SPADEVehicleAgent(Agent):
    """基于 SPADE 的车辆 Agent 实现"""

    class SignAndReportBehaviour(CyclicBehaviour):
        async def run(self):
            # 签名消息
            msg = Message(to="rsu_0@xmpp_server")
            msg.body = "safety_message_signed"
            await self.send(msg)

            # 接收认证结果
            reply = await self.receive(timeout=10)
            if reply:
                print(f"认证结果: {reply.body}")

    async def setup(self):
        b = self.SignAndReportBehaviour()
        self.add_behaviour(b)
```

---

## 6. 阶段三：改进实验

### 6.1 消融实验设计

消融实验是验证 Agent 协同价值的关键，设计思路如下：

| 实验编号 | 配置 | 验证目标 |
|----------|------|----------|
| E0 | 基线方案（无 Agent） | 基准性能 |
| E1 | 加入 Vehicle Agent（本地异常检测） | 验证分层检测增益 |
| E2 | E1 + RSU Agent（自适应撤销） | 验证策略自适应增益 |
| E3 | E2 + TA Agent（门限追责） | 验证去中心化追责增益 |
| E4 | E3 + Blockchain Agent（链上审计） | 完整方案性能 |

```python
# 消融实验示例代码
from simulation.run_simulation import run_simulation
from simulation.config import SCENARIOS

import random

results = {}
for scenario_name in ["S1", "S2"]:
    cfg = SCENARIOS[scenario_name]
    cfg.simulation_steps = 50

    random.seed(42)
    result = run_simulation(cfg)
    results[scenario_name] = result
    print(f"\n{scenario_name}: 追责成功率 = {result['trace_success_rate']*100:.1f}%")
```

### 6.2 参数调优

需要调优的关键参数：

| 参数 | 范围 | 影响 |
|------|------|------|
| α (本地检测权重) | 0.3–0.7 | 越高→越依赖本地检测 |
| β (邻居验证权重) | 0.1–0.4 | 越高→越依赖邻居交叉验证 |
| γ (历史信任权重) | 0.1–0.3 | 越高→信任评估越保守 |
| 门限 k | 2–n | 越高→追责安全性越强，但延迟越高 |
| 信任阈值 | 0.3–0.8 | 越低→更激进的追责触发 |

```python
# 参数扫描示例
from simulation.protocols import collaborative_trust_evaluation

best_detection_rate = 0
best_params = {}

for alpha in [0.3, 0.4, 0.5, 0.6, 0.7]:
    for beta in [0.1, 0.2, 0.3, 0.4]:
        gamma = 1.0 - alpha - beta
        if gamma < 0:
            continue

        # ... 运行实验并记录检测率 ...
        # detection_rate = ...
        # if detection_rate > best_detection_rate:
        #     best_detection_rate = detection_rate
        #     best_params = {"alpha": alpha, "beta": beta, "gamma": gamma}
```

### 6.3 进阶改进方向

| 改进方向 | 具体操作 | 对应文件 |
|----------|---------|---------|
| 替换真实密码学 | 将 SHA-256 替换为 ECC/BLS 签名 | `simulation/agents.py` 中的 `sign_message()` |
| 集成联邦学习 | 使用 Flower 框架实现联邦异常检测 | 新增 `simulation/federated.py` |
| 集成区块链 | 使用 Ganache+Solidity 替换模拟合约 | 新增 `contracts/Revocation.sol` |
| 集成 SUMO | 通过 TraCI API 获取真实交通数据 | 新增 `simulation/sumo_bridge.py` |
| 强化学习策略 | 用 Multi-Armed Bandit 优化策略选择 | 扩展 `RSUAgent.select_revocation_strategy()` |

---

## 7. 实验结果记录与对比

### 7.1 推荐图表

以下是投稿 GLOBECOM 或撰写技术报告时推荐的核心图表：

1. **追责延迟 vs TA 数量**（折线图）—— 展示门限追责的可扩展性
2. **撤销策略切换下的验证延迟对比**（柱状图）—— 展示自适应策略增益
3. **不同车辆规模下的通信开销**（折线图）—— 展示可扩展性
4. **消融实验：E0–E4 各项指标对比**（分组柱状图）—— 核心创新验证
5. **信任评估收敛曲线**（折线图）—— 展示信任分从初始值稳定的过程

### 7.2 结果模板

```markdown
| 方案 | 追责延迟(ms) | 追责成功率(%) | 撤销延迟(ms) | 通信开销(KB/s) | 检测率(%) |
|------|------------|-------------|------------|--------------|---------|
| 基线（无Agent） | | | | | |
| +Vehicle Agent | | | | | |
| +RSU Agent | | | | | |
| +TA Agent | | | | | |
| 完整方案 | | | | | |
```

---

## 8. 常见问题

### Q1: Charm-Crypto 安装失败怎么办？

```bash
# 确保安装了系统依赖
sudo apt-get install -y libgmp-dev libssl-dev python3-dev

# 如果 pip 安装失败，尝试从源码编译
git clone https://github.com/JHUISI/charm.git
cd charm
pip install -e .
```

### Q2: 仿真结果与论文数据不一致？

常见原因：
1. **曲线参数不同**：确保使用论文指定的曲线（如 MNT-224 或 BN-256）
2. **硬件差异**：记录你的 CPU 型号和内存，与论文的实验环境对比
3. **库版本差异**：PBC Library 和 Charm-Crypto 不同版本的性能有差异
4. **批量大小**：确保测试的消息数量与论文一致

### Q3: Agent 协同引入了多少额外开销？

Agent 间通信开销取决于：
- 消息格式（protobuf < JSON < XML）
- 通信频率（每步通信 vs 按需通信）
- Agent 数量

典型开销参考：
- XMPP 消息：~200 bytes/条
- gRPC 调用：~100 bytes/条（protobuf 编码）
- 联邦学习模型更新：~10 KB/轮（LSTM 参数）

### Q4: 如何选择 Agent 框架？

| 阶段 | 推荐框架 | 理由 |
|------|----------|------|
| 原型验证 | SPADE | Python 原生，与 Charm-Crypto 兼容 |
| 大规模仿真 | Mesa | 支持 >1000 Agent，可视化好 |
| 性能测试 | 自定义 (asyncio+gRPC) | 延迟最低，可与 SUMO/NS-3 集成 |

### Q5: 如何将结果用于论文投稿？

参考 [GLOBECOM 投稿指南](globecom_submission_guide.md) 中的详细建议，包括：
- 实验对比维度与指标选取
- 推荐仿真环境配置
- 论文结构与撰写策略
