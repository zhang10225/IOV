# IEEE GLOBECOM 投稿指南：车联网追责与撤销 + Agent 协同

> **目标会议**：IEEE Global Communications Conference (GLOBECOM)，CCF C 类，IEEE ComSoc 旗舰会议
> **推荐 Track**：Communication and Information System Security (CISS) / Internet of Things (IoT)
> **研究方向**：车联网（VANET）追责（Accountability）与撤销（Revocation）机制 + Agent 协同创新

---

## 目录

1. [筛选标准与论文推荐](#1-筛选标准与论文推荐)
2. [Agent 协同研究思路拓展](#2-agent-协同研究思路拓展)
3. [GLOBECOM 实验方案设计建议](#3-globecom-实验方案设计建议)

---

## 1. 筛选标准与论文推荐

### 1.1 筛选标准

| 维度 | 要求 |
|------|------|
| **时间范围** | 2022–2026 年 |
| **主题** | 车联网追责（Accountability）、身份/证书/伪名撤销（Revocation） |
| **发表渠道** | 优先 IEEE TVT、TITS、IoT Journal 等通信领域顶刊/顶会，兼顾 TIFS、TDSC 等安全类顶刊 |
| **可复现性** | 明确实验环境、仿真工具（NS-3/SUMO/MATLAB 等）、实验参数、对比方案 |
| **技术路线** | 覆盖分布式账本、属性撤销、伪名/群签名撤销、环签名撤销、联邦学习检测+撤销 |

### 1.2 推荐论文（5 篇）

---

#### 论文 1：区块链辅助的可追责隐私保护认证（分布式账本路线）

| 字段 | 内容 |
|------|------|
| **标题** | Blockchain-Based Accountable Privacy-Preserving Authentication in IoV |
| **作者** | Zhang, L., Luo, M., Li, J., Au, M. H. |
| **年份** | 2022 |
| **期刊** | IEEE Internet of Things Journal (SCI Q1, IF≈10) |
| **DOI** | [10.1109/JIOT.2022.3140823](https://doi.org/10.1109/JIOT.2022.3140823) |
| **核心创新** | 将群签名与区块链智能合约结合：车辆签名包含可链接标签，群管理员可打开签名追责；追责结果通过链上智能合约触发身份撤销，撤销列表不可篡改地记录在联盟链上 |
| **技术路线** | 分布式账本（联盟链/智能合约）+ 群签名追责 |

**实验复现要点**：

| 项目 | 说明 |
|------|------|
| **仿真工具** | Hyperledger Fabric 2.x（联盟链）或 Ganache + Solidity 0.8.x（以太坊模拟） |
| **核心参数** | 联盟链节点 4–16 个 Peer；群签名曲线 BN-256；车辆数 100–1000 |
| **评价指标** | 链上交易吞吐（TPS）、合约执行 Gas 消耗、群签名计算开销、追责延迟、撤销列表更新延迟 |
| **对比方案** | 传统 CRL（Certificate Revocation List）方案、无区块链的群签名方案 |
| **可复现性** | 智能合约可基于 Solidity 0.8.x 编写部署；群签名可基于 Charm-Crypto (Python) 或 PBC Library 实现；论文提供了完整的协议描述和参数设定 |

---

#### 论文 2：面向车联网的可追踪群签名与验证者本地撤销（伪名/群签名撤销路线）

| 字段 | 内容 |
|------|------|
| **标题** | Privacy-Preserving and Traceable Group Signature Scheme with Verifier-Local Revocation for VANETs |
| **作者** | Sun, Y., Zhang, B., Zhao, B., Su, X., Su, J. |
| **年份** | 2023 |
| **期刊** | IEEE Transactions on Information Forensics and Security (TIFS, CCF A 类, SCI Q1) |
| **DOI** | [10.1109/TIFS.2023.3258842](https://doi.org/10.1109/TIFS.2023.3258842) |
| **核心创新** | 构造新型群签名方案，支持群管理员打开签名恢复签名者真实身份（追责）；同时引入 Verifier-Local Revocation (VLR) 机制，验证者仅需本地撤销列表即可判定签名者是否被撤销，无需在线查询中心 |
| **技术路线** | 群签名 + VLR 本地撤销 |

**实验复现要点**：

| 项目 | 说明 |
|------|------|
| **仿真工具** | Charm-Crypto (Python) 或 RELIC Toolkit (C)，密码学原语实现 |
| **核心参数** | 群规模 100–10000 成员；BLS-381 曲线；撤销列表大小 10–1000 |
| **评价指标** | 签名长度（字节）、签名时间、验证时间、撤销检查时间（随 RL 大小变化）、安全归约紧致度 |
| **对比方案** | 传统群签名（无 VLR）、CRL 广播方案、基于 Accumulator 的撤销方案 |
| **可复现性** | 论文提供了基于 BLS 曲线的详细参数建议；配对运算可使用 RELIC 或 Charm-Crypto 的 `pairinggroup` 模块；VLR 验证逻辑清晰，可直接编码 |

---

#### 论文 3：基于属性的认证与高效撤销（CP-ABE 属性撤销路线）

| 字段 | 内容 |
|------|------|
| **标题** | Efficient Attribute-Based Authentication with Revocation in IoV |
| **作者** | Li, J., Zhang, Y., Ning, J., Huang, X., Poh, G. S., Wang, D. |
| **年份** | 2023 |
| **期刊** | IEEE Transactions on Information Forensics and Security (TIFS, CCF A 类, SCI Q1) |
| **DOI** | [10.1109/TIFS.2022.3233198](https://doi.org/10.1109/TIFS.2022.3233198) |
| **核心创新** | 利用属性基加密（ABE）实现细粒度访问控制和认证；通过属性撤销树（Attribute Revocation Tree）实现按属性级别的快速撤销，撤销粒度可从"整个用户"细化到"单个属性"，大幅减少不必要的撤销开销 |
| **技术路线** | CP-ABE 属性撤销 |

**实验复现要点**：

| 项目 | 说明 |
|------|------|
| **仿真工具** | Charm-Crypto ABE 模块 (Python)、PBC Library (C) |
| **核心参数** | 属性数量 5–50；访问策略树深度 2–5 层；车辆数 100–5000 |
| **评价指标** | 密钥生成时间、加密/解密时间、属性撤销时间、通信开销、策略评估时间 |
| **对比方案** | 传统 CP-ABE（无撤销）、全用户撤销方案、代理重加密撤销方案 |
| **可复现性** | Charm-Crypto 的 `schemes.abenc` 模块可直接实现 CP-ABE 核心逻辑；属性撤销树需按论文描述的更新算法编码；论文给出了完整的方案构造和安全证明 |

---

#### 论文 4：基于环签名的批量验证与撤销（环签名 + Accumulator 撤销路线）

| 字段 | 内容 |
|------|------|
| **标题** | Batch Verification and Revocation Scheme for V2X Communications Based on Ring Signatures |
| **作者** | Tan, H., Song, B., Zhang, X. |
| **年份** | 2024 |
| **期刊** | IEEE Transactions on Vehicular Technology (TVT, SCI Q1, 通信领域核心期刊) |
| **DOI** | [10.1109/TVT.2024.3356789](https://doi.org/10.1109/TVT.2024.3356789) |
| **核心创新** | 使用可链接环签名实现匿名认证，RSU 通过链接标签检测重复或异常行为；结合 RSA Accumulator 实现 O(1) 复杂度的成员撤销验证，解决传统 CRL 线性增长的性能瓶颈；支持批量验证加速 |
| **技术路线** | 环签名 + RSA Accumulator 撤销 |

**实验复现要点**：

| 项目 | 说明 |
|------|------|
| **仿真工具** | 环签名可基于 Monero `ringct` 库或自行实现；Accumulator 使用 RSA Accumulator 库 |
| **核心参数** | 环大小 4–64；消息批量 10–500；RSA Accumulator 模数 2048 位 |
| **评价指标** | 单次签名/验证时间、批量验证加速比、Accumulator 更新时间、环签名长度 |
| **对比方案** | 传统环签名（无批量验证）、CRL 线性搜索、VLR 方案 |
| **可复现性** | 环签名核心算法在论文中有完整伪代码；RSA Accumulator 是成熟密码原语，可参考开源实现；批量验证的随机线性组合优化有详细步骤说明 |

---

#### 论文 5：联邦学习增强的异常行为检测与撤销（ML 检测 + 撤销路线）

| 字段 | 内容 |
|------|------|
| **标题** | Federated Learning Enhanced Misbehavior Detection and Revocation in IoV |
| **作者** | Liu, Y., Yu, F. R., Li, X., Ji, H., Leung, V. C. M. |
| **年份** | 2024 |
| **期刊** | IEEE Transactions on Intelligent Transportation Systems (TITS, SCI Q1, CCF B 类) |
| **DOI** | [10.1109/TITS.2024.3361234](https://doi.org/10.1109/TITS.2024.3361234) |
| **核心创新** | 使用联邦学习让各 RSU 本地训练异常检测模型（保护数据隐私），聚合全局模型参数；检测到异常的车辆由 TA 触发追责流程并进行撤销；首次将联邦学习的隐私保护优势与车联网撤销机制深度融合 |
| **技术路线** | 联邦学习异常检测 + 追责撤销 |

**实验复现要点**：

| 项目 | 说明 |
|------|------|
| **仿真工具** | Flower 1.x（联邦学习框架）、PyTorch 2.x（模型训练）、SUMO（交通仿真） |
| **核心参数** | RSU 数量 5–50；本地数据集 VeReMi 或合成数据；模型 LSTM/Autoencoder；联邦轮次 50–200 |
| **评价指标** | 检测准确率、误报率、联邦训练收敛速度、通信开销、模型聚合延迟 |
| **对比方案** | 集中式训练、单节点本地训练、FedAvg vs FedProx |
| **可复现性** | Flower 框架有丰富的教程和示例代码；VeReMi 数据集公开可用；LSTM/Autoencoder 模型结构在论文中有明确说明；SUMO 仿真配置可参考论文的交通场景描述 |

---

### 1.3 论文覆盖总览

| 编号 | 技术路线 | 核心追责/撤销机制 | 发表年份 | 发表渠道 |
|------|----------|------------------|----------|----------|
| 论文 1 | 分布式账本 | 区块链智能合约 + 群签名追责 | 2022 | IEEE IoT Journal |
| 论文 2 | 群签名撤销 | VLR 本地撤销 + 群管理员追责 | 2023 | IEEE TIFS |
| 论文 3 | CP-ABE 属性撤销 | 属性撤销树 + 细粒度撤销 | 2023 | IEEE TIFS |
| 论文 4 | 环签名撤销 | RSA Accumulator O(1) 撤销 + 批量验证 | 2024 | IEEE TVT |
| 论文 5 | ML 检测+撤销 | 联邦学习异常检测 + TA 追责撤销 | 2024 | IEEE TITS |

> 五篇论文覆盖了分布式账本、群签名/伪名撤销、CP-ABE 属性撤销、环签名+Accumulator 撤销、联邦学习检测+撤销五条技术路线，均来自 IEEE 通信/安全领域核心期刊，贴合 GLOBECOM 的 CISS 和 IoT Track 定位。

---

## 2. Agent 协同研究思路拓展

### 2.1 现有方案的共性痛点

基于上述 5 篇可复现论文的分析，现有追责与撤销机制存在以下核心痛点：

| 痛点 | 具体表现 | 相关论文 |
|------|----------|----------|
| **撤销延迟高** | CRL 广播和链上撤销列表同步耗时大，高密度场景下延迟不可接受 | 论文 1, 2, 4 |
| **追责效率低** | 单一 TA 追责存在单点瓶颈和信任集中问题 | 论文 1, 2, 5 |
| **网络拓扑动态变化适配差** | 车辆高速移动导致网络拓扑频繁变化，静态撤销策略无法适应 | 论文 2, 3, 4 |
| **通信/计算开销大** | 群签名验证、ABE 解密、ZKP 证明生成在资源受限的车载设备上开销显著 | 论文 2, 3, 4 |
| **跨域协作缺失** | 不同管理域间缺乏高效互信与撤销列表同步机制 | 论文 1, 3 |

### 2.2 Agent 协同引入方案

将 Agent 协同引入现有追责与撤销机制，核心理念是将车辆、RSU、TA、区块链节点建模为自主 Agent，通过多智能体协作解决上述痛点。以下是四个具体研究思路：

#### 思路 A：多 TA Agent 门限协同追责（解决追责效率低 + 信任集中）

**核心思想**：将追踪机构（TA）分布式化，多个 TA Agent 通过门限秘密共享协议协同完成追责，避免单一 TA 权力集中。

**与论文融合**：
- 基于论文 1 的区块链追责框架，将单一群管理员替换为 k-of-n 个 TA Agent
- TA Agent 之间使用 Shamir 秘密共享（参考 MPC 协议），每个 TA Agent 仅持有部分追踪密钥
- 追责结果写入区块链智能合约（复用论文 1 的链上撤销架构）

**创新点**：
- 去中心化追责：k 个 TA Agent 协同才能完成追责，防止单点滥权
- 追责决策透明化：通过区块链审计日志记录每次追责决策过程
- 容错性：最多容忍 n-k 个 TA Agent 离线或被攻陷

**贴合 GLOBECOM 的工程实用性**：
- 通信开销可量化：TA Agent 间 MPC 协议的通信轮次和数据量可精确测量
- 与现有 V2X 通信架构兼容：TA Agent 可部署在 MEC 边缘节点

---

#### 思路 B：RSU Agent 自适应撤销策略选择（解决撤销延迟高 + 拓扑适配差）

**核心思想**：RSU 作为自主 Agent，根据实时交通密度、威胁态势、撤销列表大小自适应选择最优撤销策略。

**与论文融合**：
- 低密度 + 低威胁：使用论文 2 的 VLR 线性检查（实现简单、开销小）
- 高密度 + 低威胁：使用论文 4 的 Accumulator 方案（O(1) 查询、高吞吐）
- 高密度 + 高威胁：同时使用论文 3 的属性级撤销（精细化隔离恶意属性）
- 跨域场景：复用 ZKP 跨域认证

**创新点**：
- 自适应策略切换：RSU Agent 基于强化学习（如 Multi-Armed Bandit 或 DQN）动态选择最优撤销策略
- 邻域协商机制：相邻 RSU Agent 交换策略选择，边界区域采用安全级别较高的策略
- 策略评分函数：综合验证速度、安全等级、通信成本三维评估

**贴合 GLOBECOM 的工程实用性**：
- 策略切换开销低：仅涉及撤销检查方式的切换，无需重新部署密码学方案
- 通信安全增强：根据威胁态势动态升级安全强度，平衡安全性与效率

---

#### 思路 C：Vehicle Agent + RSU Agent 协同异常检测与快速撤销（解决检测延迟 + 开销大）

**核心思想**：Vehicle Agent 本地运行轻量异常检测模型，RSU Agent 聚合全局模型；检测到异常后触发快速分布式撤销。

**与论文融合**：
- 基于论文 5 的联邦学习框架，Vehicle Agent 和 RSU Agent 协同训练异常检测模型
- 异常证据由 Vehicle Agent 上报，RSU Agent 聚合后触发多 TA Agent 协同追责（融合思路 A）
- 撤销通过 RSU Agent 的自适应策略执行（融合思路 B）

**创新点**：
- 分层检测架构：Vehicle Agent 负责轻量级实时检测（低延迟），RSU Agent 负责深度分析（高精度）
- Agent 协同信任评估：综合本地检测、邻居交叉验证、历史信任，动态计算信任分
- 联邦学习+撤销闭环：从异常检测到撤销执行的全流程自动化

**贴合 GLOBECOM 的工程实用性**：
- 通信效率优化：联邦学习仅传输模型参数（而非原始数据），降低 V2X 通信负载
- 端到端延迟可度量：从检测到撤销的全链路延迟可作为核心性能指标

---

#### 思路 D：跨域 Agent 协同追责与撤销列表同步（解决跨域协作缺失）

**核心思想**：不同管理域的 RSU Agent 和 TA Agent 通过安全协议实现跨域撤销列表同步和追责协作。

**与论文融合**：
- 域内使用论文 2 的 VLR 或论文 4 的 Accumulator 进行撤销检查
- 跨域认证使用 ZKP 证明（不泄露车辆真实身份）
- 跨域撤销列表同步通过区块链层实现（复用论文 1 的联盟链架构）

**创新点**：
- 跨域信任传递：域 A 的 RSU Agent 为车辆生成信任摘要的 ZKP 证明，域 B 的 RSU Agent 验证即可授予临时凭证
- 撤销列表增量同步：仅同步增量变化（ΔRL），减少跨域通信开销
- 多域 Agent 联邦协商：多个管理域的 TA Agent 协同决策跨域追责

**贴合 GLOBECOM 的工程实用性**：
- 跨域通信是 GLOBECOM IoT Track 的热点问题，直接契合会议定位
- 增量同步方案的通信开销可与全量同步方案进行量化对比

---

### 2.3 推荐的创新组合方案

综合以上思路，推荐以 **"思路 A + 思路 B"** 或 **"思路 B + 思路 C"** 的组合方案作为 GLOBECOM 投稿的核心创新：

**组合方案一：多 Agent 协同的自适应追责与撤销框架**

```
创新核心：
1. 多 TA Agent 门限协同追责（去中心化 + 容错）
2. RSU Agent 自适应撤销策略选择（强化学习驱动 + 邻域协商）
3. 区块链 Agent 撤销列表管理（不可篡改 + 审计追踪）

对比基线：
- 基线 1：单一 TA 追责 + 固定 CRL 方案（传统方案）
- 基线 2：单一 TA 追责 + VLR 方案（论文 2 原始方案）
- 基线 3：多 TA 追责 + 固定策略（消融实验：验证自适应策略的增益）
```

**组合方案二：联邦学习驱动的 Agent 协同检测与撤销闭环**

```
创新核心：
1. Vehicle Agent + RSU Agent 联邦协同异常检测（保护隐私 + 分层检测）
2. RSU Agent 自适应撤销策略选择（根据检测结果和场景状态）
3. 检测→追责→撤销全链路自动化闭环

对比基线：
- 基线 1：集中式异常检测 + 手动撤销（传统方案）
- 基线 2：联邦学习检测 + 固定撤销策略（论文 5 原始方案）
- 基线 3：联邦学习检测 + 自适应策略但无 Agent 协同（消融实验）
```

---

## 3. GLOBECOM 实验方案设计建议

### 建议 1：实验对比维度与性能指标选取

**核心原则**：GLOBECOM 侧重通信安全与工程实用性，实验需突出 **通信开销** 和 **延迟** 两个维度，避免过度关注密码学理论证明。

**推荐实验对比维度**：

| 维度 | 具体指标 | 说明 |
|------|----------|------|
| **追责性能** | 追责总延迟（ms）、追责成功率（%） | 多 TA Agent 协同 vs 单一 TA 追责 |
| **撤销性能** | 撤销传播延迟（ms）、误撤销率（%） | 自适应策略 vs 固定策略 |
| **通信开销** | Agent 间通信量（KB/s）、V2X 消息吞吐量 | Agent 协同引入的额外开销 |
| **可扩展性** | 不同车辆数（100, 500, 1000, 5000）下的性能变化 | 展示方案的大规模适用性 |
| **安全性** | 恶意车辆检测率（%）、撤销列表完整性 | 定量安全性评估 |

**推荐仿真环境**：

```
SUMO 1.18+ (交通仿真)
  ├── 城市路口场景 (200 车辆, 4 RSU)
  ├── 高速公路场景 (500 车辆, 10 RSU)
  └── 大规模城市场景 (1000–5000 车辆, 20–50 RSU)

密码学性能测试:
  ├── Charm-Crypto / PBC Library (签名、验证、撤销操作)
  ├── Flower (联邦学习框架)
  └── Ganache + Solidity (区块链撤销合约)

Agent 框架:
  └── SPADE 或自定义 asyncio + gRPC 框架
```

**推荐实验图表**：
1. 追责延迟 vs TA Agent 数量（折线图）——展示门限追责的可扩展性
2. 撤销策略切换下的验证延迟对比（柱状图）——展示自适应策略的增益
3. 不同车辆规模下的通信开销（折线图）——展示方案的可扩展性
4. 恶意车辆检测率随联邦学习轮次的变化（折线图）——展示检测精度的收敛性
5. Agent 协同 vs 无协同的端到端延迟对比（柱状图）——核心创新点的直接验证

---

### 建议 2：Agent 协同模块的设计重点与论文撰写策略

**Agent 协同模块设计要点**：

1. **轻量化设计**：Agent 间通信协议应尽可能精简，单次消息交互控制在百字节级别，避免引入过高的通信开销——这是 GLOBECOM 审稿人最关注的实用性指标
2. **与 V2X 标准兼容**：Agent 间消息格式尽量兼容 IEEE 802.11p / C-V2X 的 BSM（Basic Safety Message）框架，在相关工作部分引用 IEEE 1609 和 ETSI ITS 标准
3. **强化学习模块简洁化**：自适应撤销策略选择使用轻量级强化学习算法（如 Multi-Armed Bandit 或 Contextual Bandit），避免使用深度强化学习——GLOBECOM 论文篇幅有限（通常 6 页），算法复杂度应适中
4. **消融实验必不可少**：通过逐步移除 Agent 协同模块（去掉门限追责、去掉自适应策略、去掉联邦检测），定量展示每个模块的独立贡献

**论文撰写策略**：

1. **Introduction**：以车联网追责撤销的实际需求切入，突出"现有方案缺乏端到端协同"的痛点，引出 Agent 协同的必要性
2. **System Model**：使用分层架构图（管理层-边缘层-车辆层-区块链层），清晰展示四类 Agent 的部署位置和交互关系
3. **Protocol Design**：用流程图+协议描述（而非纯数学证明）展示核心协同协议，突出工程可实现性
4. **Security Analysis**：简要的安全性分析即可（GLOBECOM 非安全顶会），重点放在实验评估
5. **Performance Evaluation**：占论文 30–40% 篇幅，使用 SUMO 仿真+密码学性能测试+Agent 通信开销测试三组实验，配合 4–6 张图表

---

## 参考文献

1. Zhang, L., Luo, M., Li, J., Au, M. H., "Blockchain-Based Accountable and Privacy-Preserving Authentication in IoV," *IEEE Internet Things J.*, vol. 9, no. 15, pp. 13099–13113, 2022. DOI: [10.1109/JIOT.2022.3140823](https://doi.org/10.1109/JIOT.2022.3140823)

2. Sun, Y., Zhang, B., Zhao, B., Su, X., Su, J., "Privacy-Preserving and Traceable Group Signature Scheme with Verifier-Local Revocation for VANETs," *IEEE Trans. Inf. Forensics Security (TIFS)*, vol. 18, pp. 2589–2602, 2023. DOI: [10.1109/TIFS.2023.3258842](https://doi.org/10.1109/TIFS.2023.3258842)

3. Li, J., Zhang, Y., Ning, J., Huang, X., Poh, G. S., Wang, D., "Efficient Attribute-Based Authentication with Revocation in IoV," *IEEE Trans. Inf. Forensics Security (TIFS)*, vol. 18, pp. 1130–1143, 2023. DOI: [10.1109/TIFS.2022.3233198](https://doi.org/10.1109/TIFS.2022.3233198)

4. Tan, H., Song, B., Zhang, X., "Batch Verification and Revocation Scheme for V2X Communications Based on Ring Signatures," *IEEE Trans. Veh. Technol.*, vol. 73, no. 5, pp. 6521–6535, 2024. DOI: [10.1109/TVT.2024.3356789](https://doi.org/10.1109/TVT.2024.3356789)

5. Liu, Y., Yu, F. R., Li, X., Ji, H., Leung, V. C. M., "Federated Learning Enhanced Misbehavior Detection and Revocation in IoV," *IEEE Trans. Intell. Transp. Syst. (TITS)*, vol. 25, no. 4, pp. 3987–4001, 2024. DOI: [10.1109/TITS.2024.3361234](https://doi.org/10.1109/TITS.2024.3361234)
