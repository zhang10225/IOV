# IOV 多智能体协同仿真

> 车联网（IoV）追责与撤销场景下的多 Agent 协同仿真框架原型

## 快速开始

### 环境要求

- Python 3.8+（无额外依赖）

### 运行仿真

```bash
# 在项目根目录下运行
# 使用默认场景 S1（城市路口，200 车辆，4 RSU，3 TA）
python -m simulation.run_simulation

# 指定场景
python -m simulation.run_simulation --scenario S2   # 高速公路
python -m simulation.run_simulation --scenario S3   # 跨城通勤
python -m simulation.run_simulation --scenario S4   # 大规模城市

# 自定义仿真步数与随机种子
python -m simulation.run_simulation --scenario S1 --steps 200 --seed 123
```

### 运行测试

```bash
python -m pytest tests/ -v
```

## 模块结构

```
simulation/
├── __init__.py           # 包初始化
├── config.py             # 场景配置与全局参数
├── agents.py             # 四类 Agent 定义
│   ├── VehicleAgent      # 车辆层：消息签名、异常检测、证据上报
│   ├── RSUAgent          # 边缘层：认证、信任管理、自适应撤销
│   ├── TAAgent           # 管理层：门限协同追责
│   └── BlockchainAgent   # 区块链层：撤销合约、审计日志
├── protocols.py          # 三项核心协同协议
│   ├── collaborative_trust_evaluation()      # 协议一：协同信任评估
│   ├── distributed_accountability()          # 协议二：分布式追责决策
│   └── adaptive_revocation_negotiation()     # 协议三：自适应撤销策略协商
├── run_simulation.py     # 仿真主入口
└── requirements.txt      # 依赖说明
```

## 实验场景

| 场景 | 描述 | 车辆数 | RSU 数 | TA 数 | 门限 k |
|------|------|--------|--------|-------|--------|
| S1 | 城市路口 | 200 | 4 | 3 | 2 |
| S2 | 高速公路 | 500 | 10 | 3 | 2 |
| S3 | 跨城通勤 | 1,000 | 20 | 6 | 4 |
| S4 | 大规模城市 | 5,000 | 50 | 5 | 3 |

## 评价指标

- **信任评估延迟 (ms)**：协同信任评估协议的执行时间
- **恶意车辆检测率 (%)**：正确识别恶意车辆的比例
- **追责成功率 (%)**：门限协同追责的成功比例
- **追责延迟 (ms)**：从发起追责到获得真实身份的时间
- **撤销策略分布**：各 RSU 自适应选择的撤销策略统计

## 改进方向

本仿真为原型验证框架，可沿以下方向扩展：

1. **密码学原语替换**：将简化的 SHA-256 签名替换为 ECC/BLS 群签名（使用 Charm-Crypto）
2. **联邦学习集成**：在异常检测模块中集成 Flower 联邦学习框架
3. **区块链集成**：使用 Ganache + Solidity 实现真实的撤销智能合约
4. **交通仿真集成**：通过 TraCI API 对接 SUMO 交通仿真器
5. **网络仿真集成**：通过 NS-3 引入真实的无线网络延迟和丢包模型

详细改进路径请参阅 [Agent 实验指南](../docs/agent_experiment_guide.md)。
