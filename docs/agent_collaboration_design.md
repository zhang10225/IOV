# 多智能体（Agent）协同设计方案

> 面向车联网（IoV）追责与撤销场景的多Agent协同架构、协议及实现路线

---

## 目录

1. [背景与动机](#1-背景与动机)
2. [系统架构](#2-系统架构)
3. [Agent 定义与职责](#3-agent-定义与职责)
4. [核心协同协议](#4-核心协同协议)
5. [关键模块设计](#5-关键模块设计)
6. [与现有论文方案的融合点](#6-与现有论文方案的融合点)
7. [技术选型](#7-技术选型)
8. [实验设计与评价指标](#8-实验设计与评价指标)
9. [实现路线图](#9-实现路线图)

---

## 1. 背景与动机

### 1.1 现有方案的局限

文献综述中 P1–P10 各论文分别解决了车联网认证、追责、撤销中的某一环节，但存在以下共性不足：

| 局限 | 说明 |
|------|------|
| **单一组件视角** | 各方案仅优化签名/验证/撤销中的某一步，缺少端到端协同 |
| **静态策略** | 认证强度、撤销机制在部署时固定，无法根据实时威胁态势自适应调整 |
| **中心化追责** | 大多依赖单一追踪机构（TA），存在单点故障和权力集中风险 |
| **跨域隔离** | 不同管理域（如不同城市、不同运营商）间缺乏高效的互信与协作机制 |

### 1.2 Agent 协同的优势

引入多智能体系统（MAS, Multi-Agent System）可以：

- **自主决策**：各实体（车辆、RSU、TA）作为独立 Agent，根据本地状态自主行动
- **协同优化**：通过 Agent 间通信协商，实现全局最优策略
- **动态适应**：根据交通密度、威胁态势实时调整认证和撤销策略
- **去中心化**：消除单点故障，多个 TA Agent 协同完成追责

---

## 2. 系统架构

### 2.1 分层 Agent 架构

```
┌─────────────────────────────────────────────────────────────┐
│                     管理层（Management Layer）                │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐ │
│  │  TA Agent 1  │  │  TA Agent 2  │  │  TA Agent k (门限)   │ │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬───────────┘ │
│         │                │                     │             │
│         └────────────────┼─────────────────────┘             │
│                          │ MPC 追责协议                       │
├──────────────────────────┼──────────────────────────────────┤
│                     边缘层（Edge Layer）                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │RSU Agent │  │RSU Agent │  │RSU Agent │  │RSU Agent │    │
│  │  (区域1)  │  │  (区域2)  │  │  (区域3)  │  │  (区域n)  │    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
│       │              │              │              │          │
│       └──────────────┴──────────────┴──────────────┘          │
│              Agent 间消息传递 / 联邦学习聚合                     │
├──────────────────────────────────────────────────────────────┤
│                     车辆层（Vehicle Layer）                    │
│  ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐         │
│  │Veh Agt│ │Veh Agt│ │Veh Agt│ │Veh Agt│ │Veh Agt│  ...    │
│  └───────┘ └───────┘ └───────┘ └───────┘ └───────┘         │
├──────────────────────────────────────────────────────────────┤
│                  区块链层（Blockchain Layer）                  │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  Blockchain Agent（智能合约执行、撤销列表存储、审计日志）  │    │
│  └──────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 架构说明

| 层级 | Agent 类型 | 数量 | 职责概述 |
|------|-----------|------|----------|
| 管理层 | TA Agent | k 个（门限） | 协同追责、身份还原、全局策略下发 |
| 边缘层 | RSU Agent | n 个（按区域） | 本地认证验证、信任评估、自适应撤销策略选择、联邦学习本地训练 |
| 车辆层 | Vehicle Agent | 动态（50–5000） | 消息签名、邻居交互、本地异常检测、证据上报 |
| 区块链层 | Blockchain Agent | 1 个（逻辑） | 智能合约执行、撤销列表维护、追责记录存储 |

---

## 3. Agent 定义与职责

> 以下使用 Python 伪代码描述各 Agent 的状态与动作接口，实际实现时应使用 dataclass 或协议基类。

### 3.1 Vehicle Agent（车辆智能体）

```python
class VehicleAgent:
    """车辆层智能体——负责消息签名、邻居监测和证据上报"""

    state = {
        "pseudo_id": str,          # 当前使用的假名
        "trust_score": float,      # 被 RSU 评定的信任分（0.0 ~ 1.0）
        "neighbors": list,         # 通信范围内的邻居列表
        "local_model": object,     # 本地异常检测模型（轻量 LSTM/Autoencoder）
    }

    actions = [
        "sign_message(msg)",           # 使用当前假名对消息签名
        "verify_neighbor(msg, sig)",   # 验证邻居消息
        "detect_anomaly(msg_stream)",  # 本地异常检测
        "report_evidence(vehicle_id, evidence)",  # 向 RSU 上报异常证据
        "request_new_pseudonym()",     # 请求新假名
    ]
```

### 3.2 RSU Agent（路侧单元智能体）

```python
class RSUAgent:
    """边缘层智能体——负责区域认证、信任管理和自适应撤销"""

    state = {
        "region_id": str,                   # 所属区域
        "vehicle_registry": dict,           # 区域内车辆注册表
        "trust_table": dict,                # 车辆信任分表
        "traffic_density": float,           # 当前交通密度
        "threat_level": str,                # 威胁态势（low/medium/high）
        "revocation_strategy": str,         # 当前撤销策略
        "federated_model": object,          # 联邦学习全局模型
    }

    actions = [
        "authenticate_vehicle(veh_id, credential)",    # 认证车辆
        "update_trust_score(veh_id, evidence)",        # 更新信任分
        "select_revocation_strategy()",                # 自适应选择撤销策略
        "broadcast_revocation(revoked_id)",            # 广播撤销信息
        "aggregate_federated_model(local_updates)",    # 聚合联邦学习模型
        "negotiate_with_neighbors(rsu_agents, topic)", # 与邻近 RSU 协商
    ]
```

### 3.3 TA Agent（追踪机构智能体）

```python
class TAAgent:
    """管理层智能体——协同追责与身份还原"""

    state = {
        "ta_id": str,                   # TA 标识
        "secret_share": bytes,          # 门限密钥份额
        "threshold_k": int,             # 追责门限（需 k 个 TA 协同）
        "total_n": int,                 # TA 总数
        "tracing_requests": queue,      # 待处理追责请求队列
    }

    actions = [
        "receive_tracing_request(evidence)",        # 接收追责请求
        "compute_partial_trace(encrypted_id)",      # 计算部分追踪结果
        "collaborate_trace(other_ta_agents)",       # 与其他 TA 协同完成追踪
        "submit_revocation(real_id)",               # 提交撤销至区块链
        "update_global_policy(policy)",             # 更新全局策略
    ]
```

### 3.4 Blockchain Agent（区块链智能体）

```python
class BlockchainAgent:
    """区块链层智能体——执行合约、维护撤销列表"""

    state = {
        "revocation_list": set,          # 当前撤销列表
        "audit_log": list,               # 审计日志
        "smart_contracts": dict,         # 已部署的智能合约
    }

    actions = [
        "execute_revocation_contract(real_id, evidence)",  # 执行撤销合约
        "query_revocation_status(pseudo_id)",               # 查询撤销状态
        "log_accountability_event(event)",                  # 记录追责事件
        "sync_revocation_list(rsu_agents)",                 # 同步撤销列表至 RSU
    ]
```

---

## 4. 核心协同协议

### 4.1 协议一：协同信任评估（Collaborative Trust Evaluation）

**参与者**：Vehicle Agent ↔ RSU Agent ↔ RSU Agent（邻域）

**目标**：综合本地观测与邻域信息，动态计算车辆信任分并调整认证强度。

```
步骤 1: Vehicle Agent 在本地运行轻量异常检测模型，对邻居消息进行评分
步骤 2: Vehicle Agent 将异常证据（不含明文身份）上报给所属 RSU Agent
步骤 3: RSU Agent 聚合区域内所有 Vehicle Agent 的上报信息，更新信任分表
         trust_score[v] = α × local_score + β × neighbor_reports + γ × history
步骤 4: RSU Agent 与邻近 RSU Agent 交换边界车辆的信任摘要（差分隐私保护）
步骤 5: RSU Agent 根据信任分动态调整认证策略：
         - trust_score > 0.8: 快速认证（仅验证签名）
         - 0.5 < trust_score ≤ 0.8: 标准认证（签名 + 属性验证）
         - trust_score ≤ 0.5: 增强认证（签名 + 属性 + ZKP 身份证明）
         注：阈值 0.8 / 0.5 为初始推荐值，需通过实验场景 S1–S4 调优
```

### 4.2 协议二：分布式追责决策（Distributed Accountability Decision）

**参与者**：RSU Agent → TA Agent (×k) → Blockchain Agent

**目标**：去中心化追责，避免单一 TA 权力集中。

```
步骤 1: RSU Agent 收集足够的异常证据后，向管理层发起追责请求
步骤 2: 追责请求广播至所有 TA Agent（共 n 个）
步骤 3: 每个 TA Agent 独立审核证据的有效性
         - 若证据不足，拒绝并反馈理由
         - 若证据充分，使用自己的密钥份额计算部分追踪结果
步骤 4: 当至少 k 个 TA Agent 完成部分计算后，通过 MPC 协议合成完整追踪结果
         real_id = Reconstruct(partial_trace_1, ..., partial_trace_k)  // Shamir 秘密恢复
步骤 5: 追踪结果提交至 Blockchain Agent，触发撤销智能合约
步骤 6: Blockchain Agent 更新链上撤销列表，并通知所有 RSU Agent 同步
```

### 4.3 协议三：自适应撤销策略协商（Adaptive Revocation Negotiation）

**参与者**：RSU Agent ↔ RSU Agent（邻域） ↔ Blockchain Agent

**目标**：根据实时场景自动选择最优撤销机制。

```
步骤 1: 每个 RSU Agent 监测本地状态向量:
         state_vector = (traffic_density, threat_level, revocation_list_size, latency_budget)
步骤 2: RSU Agent 根据本地状态选择候选撤销策略:
         策略映射规则:
         - 低密度 + 低威胁 → VLR 线性检查（P3，实现简单）
         - 高密度 + 低威胁 → 布隆过滤器（P4，O(1) 查询）
         - 高密度 + 高威胁 → Accumulator（P3改进，O(1) + 防假阳性）
         - 跨域场景      → ZKP 验证（P9，零知识跨域互认）
步骤 3: 邻近 RSU Agent 交换各自的策略选择
步骤 4: 边界区域的 RSU Agent 进行协商:
         - 若策略一致，直接采用
         - 若策略不一致，采用安全级别较高的策略（取并集原则）
步骤 5: 协商结果同步至 Blockchain Agent，更新全局策略参数
```

### 4.4 协议四：跨域认证协商（Cross-Domain Authentication Negotiation）

**参与者**：RSU Agent (域A) ↔ RSU Agent (域B) ↔ Vehicle Agent

**目标**：车辆跨管理域时，实现高效的身份互认。

```
步骤 1: Vehicle Agent 从域 A 移动至域 B 边界
步骤 2: 域 B 的 RSU Agent 检测到新车辆，查询是否有跨域认证缓存
步骤 3: 若无缓存，域 B RSU Agent 向域 A RSU Agent 发送认证请求
步骤 4: 域 A RSU Agent 返回该车辆的信任摘要（ZKP 证明，不泄露真实身份）:
         proof = ZKP.prove(trust_score > threshold, without revealing identity)
步骤 5: 域 B RSU Agent 验证 ZKP 证明:
         - 验证通过: 授予临时域内凭证，信任分继承
         - 验证失败: 要求 Vehicle Agent 重新完成完整认证流程
步骤 6: 认证结果写入 Blockchain Agent 的跨域审计日志
```

---

## 5. 关键模块设计

### 5.1 信任评估模块

```
输入: 车辆行为序列 B = {b_1, b_2, ..., b_t}
处理:
  1. 本地模型推理: anomaly_score = LocalModel.predict(B)
  2. 邻居交叉验证: cross_score = mean(neighbor_reports)
  3. 历史衰减加权: history_score = Σ(decay^i × past_score_i)
  4. 综合评分: trust = α·(1-anomaly_score) + β·cross_score + γ·history_score
     其中 α + β + γ = 1
     初始推荐值 α=0.5, β=0.3, γ=0.2（本地检测权重最高；需通过 S1–S4 场景实验调优）
输出: trust_score ∈ [0.0, 1.0]
```

### 5.2 自适应策略选择模块

```
输入: 本地状态向量 S = (density, threat, rl_size, latency)
处理:
  1. 策略评分函数（为每种候选策略打分）:
     score(strategy, S) = w1·verification_speed(strategy, S)
                        + w2·security_level(strategy, S)
                        + w3·communication_cost(strategy, S)
  2. 选择最高分策略: best = argmax_{strategy}(score(strategy, S))
  3. 与邻域协商（取安全级别较高者）
输出: selected_strategy ∈ {VLR, BloomFilter, Accumulator, ZKP}
```

### 5.3 门限追责模块

```
前提: n 个 TA Agent, 门限 k (k ≤ n)
密钥设置:
  1. 可信初始化阶段: 使用 Shamir (k,n) 秘密共享将主追踪密钥 sk 分为 n 份
     shares = ShamirSplit(sk, k, n) → {s_1, s_2, ..., s_n}
追责流程:
  1. RSU Agent 提交追责请求 req = (pseudo_id, evidence, timestamp)
  2. 每个 TA Agent_i 验证 evidence 后计算部分结果:
     partial_i = PartialTrace(s_i, pseudo_id)
  3. 收集 k 个 partial 后重建:
     real_id = ShamirReconstruct(partial_1, ..., partial_k)
  4. 提交 (real_id, evidence) 至 Blockchain Agent
```

---

## 6. 与现有论文方案的融合点

| 本方案模块 | 融合论文 | 具体融合方式 |
|-----------|---------|-------------|
| Vehicle Agent 签名 | P1 (ECC签名) | 车辆Agent使用P1的条件隐私签名作为基础消息签名方案 |
| Vehicle Agent 异常检测 | P10 (联邦学习) | 车辆Agent运行P10的轻量LSTM模型进行本地异常检测 |
| RSU Agent 认证 | P5 (属性认证) | RSU Agent执行P5的属性基认证，结合信任分动态调整属性要求 |
| RSU Agent 撤销 | P3 + P4 | RSU Agent根据场景在P3的VLR和P4的布隆过滤器间自适应切换 |
| RSU Agent 联邦学习 | P10 (Flower) | RSU Agent作为联邦学习的聚合节点，聚合Vehicle Agent的模型更新 |
| TA Agent 追责 | P6 (MPC) | 多个TA Agent使用P6的Shamir秘密共享实现门限追责 |
| TA Agent 策略 | P7 (参数更新) | TA Agent下发全局策略时参考P7的树形广播优化 |
| Blockchain Agent | P2 (智能合约) | 使用P2的区块链追责合约作为Blockchain Agent的执行引擎 |
| 跨域认证 | P9 (ZKP) | 跨域Agent互认使用P9的零知识证明保护隐私 |
| 批量验证 | P8 (环签名) | 高密度场景下Vehicle Agent批量消息使用P8的批量验证加速 |

---

## 7. 技术选型

### 7.1 Agent 框架

| 选项 | 说明 | 推荐场景 |
|------|------|----------|
| **SPADE** (Python) | 基于 XMPP 协议的多智能体平台，支持异步消息传递和行为树 | 快速原型验证，与Charm-Crypto/Flower无缝集成 |
| **Mesa** (Python) | Agent-Based Modeling框架，支持空间模型和数据收集 | 大规模仿真（>1000 Agent），可视化分析 |
| **自定义轻量框架** | 基于 asyncio + ZeroMQ/gRPC 的最小Agent框架 | 与SUMO/NS-3深度集成，性能优先 |

**推荐**：阶段一使用 **SPADE** 进行快速原型验证；阶段二迁移至**自定义轻量框架**与 SUMO/NS-3 集成。

### 7.2 Agent 间通信

| 方案 | 延迟 | 吞吐 | 适用场景 |
|------|------|------|----------|
| XMPP (SPADE内置) | 中 | 中 | 原型阶段，开发效率高 |
| ZeroMQ | 低 | 高 | 同机/同局域网高频消息 |
| gRPC | 低 | 高 | 跨节点结构化通信，支持 protobuf |
| MQTT | 低 | 中 | 模拟 V2X 发布/订阅通信模式 |

**推荐**：原型阶段用 XMPP；性能测试阶段用 **gRPC**（Agent间RPC调用）+ **MQTT**（模拟V2X广播）。

### 7.3 仿真集成

```
SUMO (交通流) ←→ TraCI API ←→ Agent Framework (Python)
                                    ↕
                              NS-3 (网络延迟) ←→ Tap Bridge
```

- 使用 SUMO 的 TraCI 接口控制车辆移动，每个 SUMO 车辆对应一个 Vehicle Agent
- NS-3 提供真实的无线网络延迟和丢包模型
- Agent 框架通过 TraCI 读取车辆位置，通过 NS-3 模拟通信延迟

---

## 8. 实验设计与评价指标

### 8.1 实验场景

| 场景 | 描述 | 车辆数 | RSU 数 | TA 数 |
|------|------|--------|--------|-------|
| S1: 城市路口 | 单一管理域，中密度交通 | 200 | 4 | 3 (k=2) |
| S2: 高速公路 | 单一管理域，高速移动 | 500 | 10 | 3 (k=2) |
| S3: 跨城通勤 | 双管理域，车辆跨域频繁 | 1000 | 20 (每域10) | 6 (每域3) |
| S4: 大规模城市 | 单域高密度压力测试 | 5000 | 50 | 5 (k=3) |

### 8.2 评价指标

| 类别 | 指标 | 说明 |
|------|------|------|
| **认证性能** | 平均认证延迟 (ms) | 从车辆发起认证到获得结果的时间 |
| | 认证吞吐量 (次/秒) | RSU Agent 每秒处理的认证请求数 |
| **追责性能** | 追责总延迟 (ms) | 从发起追责到获得真实身份的时间 |
| | 追责成功率 (%) | k个TA协同追责的成功比例 |
| **撤销性能** | 撤销传播延迟 (ms) | 从撤销决策到所有RSU同步完成的时间 |
| | 误撤销率 (%) | 正常车辆被错误撤销的比例 |
| **协同开销** | Agent 间通信量 (KB/s) | Agent 间协同产生的额外通信开销 |
| | 策略协商延迟 (ms) | RSU Agent 间完成策略协商的时间 |
| **信任评估** | 恶意车辆检测率 (%) | 正确识别恶意车辆的比例 |
| | 信任评估收敛时间 (s) | 信任分从初始值稳定至准确值的时间 |
| **跨域** | 跨域认证延迟 (ms) | 车辆进入新域到获得认证的时间 |

### 8.3 对比基线

| 基线 | 说明 |
|------|------|
| **无Agent（独立方案）** | 直接使用P1–P10中的单一方案，无Agent协同 |
| **集中式Agent** | 单一中央控制器替代分布式Agent协同 |
| **静态策略** | Agent存在但不进行自适应策略切换 |

---

## 9. 实现路线图

```
阶段 1: Agent 原型验证（2 周）
├── 使用 SPADE 实现四类 Agent 的基本框架
├── 实现 Agent 间消息传递（XMPP）
├── 实现协同信任评估协议（协议一）
├── 单元测试：验证 Agent 状态转换和消息交互
└── 在小规模场景（20 车辆, 2 RSU）上验证基本功能

阶段 2: 核心协议实现（3 周）
├── 实现分布式追责决策协议（协议二）
│   ├── 集成 Shamir 秘密共享（基于 P6 的 MP-SPDZ）
│   └── 实现多 TA Agent 门限追责流程
├── 实现自适应撤销策略协商（协议三）
│   ├── 集成 P3 VLR / P4 布隆过滤器 / P8 Accumulator
│   └── 实现策略评分与协商逻辑
├── 实现跨域认证协商协议（协议四）
│   └── 集成 P9 的 ZKP 跨域证明
└── 集成测试：多协议联合运行

阶段 3: 仿真集成与评估（3 周）
├── 将 Agent 框架与 SUMO TraCI 接口对接
├── 配置 NS-3 网络仿真环境
├── 在 S1–S4 四个实验场景下运行完整实验
├── 收集全部评价指标，与三组基线对比
└── 生成实验报告与可视化图表

阶段 4: 优化与论文撰写（2 周）
├── 根据实验结果优化 Agent 协同参数（α, β, γ, 门限 k 等）
├── 性能瓶颈分析与优化（通信开销、计算开销）
├── 撰写技术报告或学术论文
└── 代码与文档整理，开源发布
```

**总预计工期**：10 周（可与文献综述中阶段 1–2 的基础复现和对比实验并行推进，阶段 3–4 共享仿真环境）。
