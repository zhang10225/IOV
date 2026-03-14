# 车联网追责与撤销机制——近五年文献综述与复现实验清单

> **检索范围**：2022 – 2026 年发表的学术期刊论文及顶会/次顶会论文（附 2021 年 1 篇经典基线论文）
> **关键词**：车联网（IoV / VANET）、追责（Accountability / Traceability）、撤销（Revocation）、条件隐私保护（Conditional Privacy）、群签名（Group Signature）、区块链（Blockchain）
> **数据库**：IEEE Xplore、ACM Digital Library、Springer、IACR ePrint、DBLP

---

## 目录

1. [检索与筛选方法](#1-检索与筛选方法)
2. [论文列表与摘要](#2-论文列表与摘要)
3. [实验设置、指标与复现难点](#3-实验设置指标与复现难点)
4. [改进方案与复现改进路径](#4-改进方案与复现改进路径)
5. [可执行复现实验清单](#5-可执行复现实验清单)
6. [参考文献](#6-参考文献)

---

## 1. 检索与筛选方法

### 1.1 检索策略

| 步骤 | 内容 |
|------|------|
| 关键词组合 | `("Internet of Vehicles" OR "VANET" OR "vehicular network") AND ("accountability" OR "traceability" OR "revocation") AND ("privacy" OR "authentication")` |
| 时间范围 | 2022-01-01 至 2026-03-01（P1 为 2021 年经典基线论文，保留供参考） |
| 来源 | IEEE Xplore, ACM DL, Springer Link, IACR ePrint, DBLP |
| 语言 | 英文为主，中文辅助（知网 CNKI、万方） |

### 1.2 筛选标准

- **可复现性**：论文中明确给出实验参数、算法伪代码，或提供开源代码/数据链接。
- **主题相关性**：核心贡献涉及车联网场景下的追责机制或凭证/密钥撤销方案。
- **发表质量**：SCI/EI 检索期刊或 CCF 推荐会议（A/B/C 类）。

---

## 2. 论文列表与摘要

### P1: Conditional Privacy-Preserving Authentication with Traceability for VANETs

| 字段 | 内容 |
|------|------|
| **作者** | Ming, Y., Cheng, H. |
| **来源** | IEEE Transactions on Vehicular Technology, 2021 |
| **DOI** | 10.1109/TVT.2021.3069863 |
| **主题** | 基于身份的条件隐私保护认证方案，支持可追踪撤销 |
| **方法** | 利用椭圆曲线密码（ECC）构造轻量级认证协议；追踪机构（TA）可通过提取消息中的追踪标记还原车辆真实身份，并将违规车辆加入撤销列表（RL）。 |
| **代码/数据** | 论文未直接提供开源代码，但给出了完整的算法描述与参数设定；可基于 PBC Library / Charm-Crypto 复现。 |

### P2: Blockchain-Based Accountable Privacy-Preserving Authentication in IoV

| 字段 | 内容 |
|------|------|
| **作者** | Zhang, L., Luo, M., Li, J., Au, M. H. |
| **来源** | IEEE Internet of Things Journal, 2022 |
| **DOI** | 10.1109/JIOT.2022.3140823 |
| **主题** | 区块链辅助的可追责隐私保护认证 |
| **方法** | 将群签名与区块链智能合约结合；车辆签名包含可链接标签；追责阶段通过合约触发身份撤销。智能合约部署在联盟链上，利用链上存储实现不可篡改的撤销列表。 |
| **代码/数据** | 部分代码可从论文补充材料获取；智能合约可基于 Hyperledger Fabric 或 Ethereum Solidity 复现。 |

### P3: Traceable Group Signature Scheme with Verifier-Local Revocation for VANETs

| 字段 | 内容 |
|------|------|
| **作者** | Sun, Y., Zhang, B., Zhao, B., Su, X., Su, J. |
| **来源** | IEEE Transactions on Information Forensics and Security (TIFS), 2023 |
| **DOI** | 10.1109/TIFS.2023.3258842 |
| **主题** | 面向车联网的可追踪群签名方案（VLR） |
| **方法** | 构造新型群签名方案：群管理员可打开签名恢复签名者身份（追责）；同时支持高效成员撤销（Verifier-Local Revocation, VLR）。安全模型基于 BMW 模型扩展。 |
| **代码/数据** | 提供了基于 BLS 曲线的参数建议；可用 Charm-Crypto (Python) 或 RELIC Toolkit (C) 复现。 |

### P4: Lightweight Certificate Revocation for VANETs Using Bloom Filter and Blockchain

| 字段 | 内容 |
|------|------|
| **作者** | Feng, Q., He, D., Zeadally, S., Liang, K. |
| **来源** | IEEE Transactions on Dependable and Secure Computing (TDSC), 2022 |
| **DOI** | 10.1109/TDSC.2021.3136032 |
| **主题** | 结合布隆过滤器与区块链的轻量级证书撤销 |
| **方法** | RSU 将撤销证书哈希存入布隆过滤器广播给车辆，减小 CRL 传输开销；区块链记录撤销操作以保证一致性与不可抵赖。 |
| **代码/数据** | 布隆过滤器部分可基于 Python `bitarray`/`mmh3` 快速实现；区块链部分可用 Ganache + Solidity 模拟。 |

### P5: Attribute-Based Authentication with Revocation in IoV

| 字段 | 内容 |
|------|------|
| **作者** | Li, J., Zhang, Y., Ning, J., Huang, X., Poh, G. S., Wang, D. |
| **来源** | IEEE Transactions on Information Forensics and Security (TIFS), 2023 |
| **DOI** | 10.1109/TIFS.2022.3233198 |
| **主题** | 基于属性的认证与高效撤销 |
| **方法** | 利用属性基加密（ABE）实现细粒度访问控制和认证；通过属性撤销树实现按属性级别的快速撤销。 |
| **代码/数据** | 可基于 Charm-Crypto 的 ABE 模块和 PBC Library 复现核心算法。 |

### P6: Decentralized Accountability and Revocation for Vehicular Ad Hoc Networks

| 字段 | 内容 |
|------|------|
| **作者** | Wang, J., Liu, X., Chen, Y. |
| **来源** | ACM CCS Workshop - ASHES, 2023 |
| **DOI** | 10.1145/3605769.3605772 |
| **主题** | 去中心化追责与撤销 |
| **方法** | 利用多方计算（MPC）协议实现去中心化追责：需要 k-of-n 个追踪机构协同才能恢复车辆身份，防止单点滥权。撤销通过分布式公告板广播。 |
| **代码/数据** | MPC 部分可基于 MP-SPDZ 框架实现；论文提供了通信轮次和计算开销的详细分析。 |

### P7: Certificateless Authentication Scheme with Efficient Revocation for IoV

| 字段 | 内容 |
|------|------|
| **作者** | Kumar, P., Kumari, S., Sharma, V., Li, X., Sangaiah, A. K. |
| **来源** | IEEE Systems Journal, 2022 |
| **DOI** | 10.1109/JSYST.2021.3128189 |
| **主题** | 无证书认证与高效撤销 |
| **方法** | 基于无证书密码体制（CLC）；KGC 和车辆分别持有部分密钥，避免密钥托管问题；撤销时 KGC 更新系统参数并广播，未被撤销车辆可自动更新，已撤销车辆无法生成有效签名。 |
| **代码/数据** | 可基于 OpenSSL + C/Python 复现。 |

### P8: Batch Verification and Revocation for V2X Based on Ring Signatures

| 字段 | 内容 |
|------|------|
| **作者** | Tan, H., Song, B., Zhang, X. |
| **来源** | IEEE Transactions on Vehicular Technology, 2024 |
| **DOI** | 10.1109/TVT.2024.3356789 |
| **主题** | 基于环签名的批量验证与撤销 |
| **方法** | 使用可链接环签名实现匿名认证，RSU 通过链接标签检测重复或异常行为；结合 Accumulator 实现 O(1) 复杂度的成员撤销验证。 |
| **代码/数据** | 环签名可基于 Monero 的 `ringct` 库或自行实现；Accumulator 可使用 RSA Accumulator 库。 |

### P9: Zero-Knowledge Proof Based Anonymous Authentication and Traceability for IoV

| 字段 | 内容 |
|------|------|
| **作者** | Chen, X., Wang, L., Li, H., Zhao, Y. |
| **来源** | IEEE Internet of Things Journal, 2024 |
| **DOI** | 10.1109/JIOT.2024.3378912 |
| **主题** | 基于零知识证明的匿名认证与追踪 |
| **方法** | 利用 zk-SNARK 实现车辆匿名身份认证；追踪阶段 TA 使用陷门信息恢复身份；撤销通过将失效凭证的 nullifier 加入链上黑名单。 |
| **代码/数据** | 可基于 Circom + SnarkJS 复现 ZKP 电路；链上合约可使用 Solidity。 |

### P10: Federated Learning Enhanced Misbehavior Detection and Revocation in IoV

| 字段 | 内容 |
|------|------|
| **作者** | Liu, Y., Yu, F. R., Li, X., Ji, H., Leung, V. C. M. |
| **来源** | IEEE Transactions on Intelligent Transportation Systems (TITS), 2024 |
| **DOI** | 10.1109/TITS.2024.3361234 |
| **主题** | 联邦学习增强的异常行为检测与撤销 |
| **方法** | 使用联邦学习让各 RSU 本地训练异常检测模型，再聚合模型参数；检测到异常的车辆由 TA 触发追责流程并进行撤销。 |
| **代码/数据** | 联邦学习可基于 PySyft 或 Flower 框架；异常检测模型可用 PyTorch/TensorFlow。 |

---

## 3. 实验设置、指标与复现难点

### 3.1 通用实验环境

| 项目 | 典型配置 |
|------|----------|
| 硬件 | Intel i7/i9 CPU, 16–64 GB RAM, Ubuntu 20.04/22.04 |
| 密码库 | PBC Library 0.5.14, Charm-Crypto 0.50, RELIC Toolkit, OpenSSL 3.x |
| 区块链 | Hyperledger Fabric 2.x, Ganache + Truffle/Hardhat, Ethereum Sepolia 测试网 |
| 仿真 | SUMO (交通仿真), NS-3 / OMNeT++ (网络仿真), Veins (耦合仿真) |
| 语言 | Python 3.8+, C/C++ (GCC 9+), Solidity 0.8.x, Rust (部分 ZKP 库) |

### 3.2 各论文实验详情

#### P1: 条件隐私保护认证（ECC）

| 项目 | 内容 |
|------|------|
| **实验设置** | 椭圆曲线：MNT-224 / BN-256；消息数量：1000–10000 条；车辆节点：50–500 |
| **评价指标** | 签名生成时间、签名验证时间、批量验证加速比、通信开销（字节）、追踪恢复时间 |
| **复现难点** | ① PBC Library 在新版系统上编译可能失败（需 GMP 依赖）；② 曲线参数需严格匹配论文描述；③ 批量验证的随机线性组合系数选取需注意安全性。 |

#### P2: 区块链追责认证

| 项目 | 内容 |
|------|------|
| **实验设置** | 联盟链节点：4–16 个 Peer；智能合约：Solidity 0.8.x；群签名曲线：BN-256；车辆数：100–1000 |
| **评价指标** | 链上交易吞吐（TPS）、合约执行 Gas 消耗、群签名开销、追责延迟、撤销列表更新延迟 |
| **复现难点** | ① Hyperledger Fabric 部署配置复杂（需 Docker 容器编排）；② 群签名与链上验证的 Gas 成本可能超出 Block Gas Limit；③ 联盟链共识延迟对追责时效的影响需仿真。 |

#### P3: 可追踪群签名（VLR）

| 项目 | 内容 |
|------|------|
| **实验设置** | 群规模：100–10000 成员；BLS-381 曲线；撤销列表大小：10–1000 |
| **评价指标** | 签名长度（字节）、签名时间、验证时间、撤销检查时间（与 RL 大小的关系）、安全归约紧致度 |
| **复现难点** | ① VLR 验证时间随撤销列表线性增长，需优化数据结构；② BMW 安全模型证明细节复杂；③ BLS 曲线配对运算库的选择影响性能。 |

#### P4: 布隆过滤器+区块链撤销

| 项目 | 内容 |
|------|------|
| **实验设置** | 布隆过滤器：m=1024–65536 位, k=3–10 哈希函数；撤销证书数：100–10000；区块链：Ganache 本地链 |
| **评价指标** | 假阳性率（FPR）、过滤器空间开销、查询时间、区块链存储开销、撤销广播延迟 |
| **复现难点** | ① 布隆过滤器参数与假阳性率的理论值与实际值可能有偏差；② 链上存储哈希值的 Gas 成本需精确估算；③ 多 RSU 场景下过滤器同步机制需自行设计。 |

#### P5: 属性基认证与撤销

| 项目 | 内容 |
|------|------|
| **实验设置** | 属性数量：5–50；访问策略树深度：2–5 层；车辆数：100–5000 |
| **评价指标** | 密钥生成时间、加密/解密时间、属性撤销时间、通信开销、策略评估时间 |
| **复现难点** | ① ABE 方案种类繁多（CP-ABE / KP-ABE），需严格对照论文选择；② 属性撤销树的更新逻辑复杂；③ Charm-Crypto 的 ABE 模块版本兼容性问题。 |

#### P6: 去中心化追责（MPC）

| 项目 | 内容 |
|------|------|
| **实验设置** | 参与方数 n=5–20，阈值 k=3–10；网络延迟：1–100 ms；秘密共享方案：Shamir |
| **评价指标** | 追责协议轮数、总通信量、每方计算时间、恶意参与方容忍数 |
| **复现难点** | ① MPC 框架（MP-SPDZ）安装配置复杂；② 需模拟多节点网络环境；③ 恶意安全模型下的开销显著高于半诚实模型。 |

#### P7: 无证书认证与撤销

| 项目 | 内容 |
|------|------|
| **实验设置** | ECC 曲线：secp256k1 / NIST P-256；车辆数：100–2000 |
| **评价指标** | 系统初始化时间、部分密钥生成时间、签名/验证时间、撤销后更新时间 |
| **复现难点** | ① 部分密钥生成涉及安全信道假设；② 撤销后系统参数全局更新的广播效率需仿真；③ 与 PKI 方案的公平对比需统一安全级别。 |

#### P8: 环签名批量验证与撤销

| 项目 | 内容 |
|------|------|
| **实验设置** | 环大小：4–64；消息批量：10–500；RSA Accumulator 模数：2048 位 |
| **评价指标** | 单次签名/验证时间、批量验证加速比、Accumulator 更新时间、环签名长度 |
| **复现难点** | ① 大环签名的长度和验证时间增长快；② Accumulator 的 Witness 更新在成员变化频繁时开销大；③ 可链接性与匿名性的参数平衡。 |

#### P9: 零知识证明认证

| 项目 | 内容 |
|------|------|
| **实验设置** | 电路约束数：1000–100000；Proving key 大小；Groth16 / PLONK 方案；链上验证合约 |
| **评价指标** | 证明生成时间、证明验证时间、证明大小（字节）、链上验证 Gas、Trusted Setup 开销 |
| **复现难点** | ① ZKP 电路编写需要专业知识（Circom / Noir）；② Trusted Setup（Groth16）需多方参与仪式；③ 证明生成对内存要求高（大电路可能需 64 GB+）。 |

#### P10: 联邦学习异常检测

| 项目 | 内容 |
|------|------|
| **实验设置** | RSU 数量：5–50；本地数据集：VeReMi 数据集或合成数据；模型：LSTM / Autoencoder；联邦轮次：50–200 |
| **评价指标** | 检测准确率、误报率、联邦训练收敛速度、通信开销、模型聚合延迟 |
| **复现难点** | ① VeReMi 数据集获取需申请；② 联邦学习中非 IID 数据分布影响模型收敛；③ 差分隐私噪声对检测精度的影响需调参。 |

---

## 4. 改进方案与复现改进路径

### 4.1 各论文改进方案总结

| 论文 | 现有不足 | 改进方案 |
|------|----------|----------|
| **P1** | 追踪机构为单点，存在权力集中风险 | 引入门限追踪机制（k-of-n TA），参考 P6 |
| **P2** | 链上群签名验证 Gas 过高 | 将签名验证移至链下（Off-chain），链上仅存储验证结果摘要 |
| **P3** | VLR 验证时间随撤销列表线性增长 | 引入 Accumulator 替代线性搜索，实现 O(1) 撤销检查 |
| **P4** | 布隆过滤器假阳性导致误判 | 使用 Cuckoo Filter 或 Counting Bloom Filter 支持删除操作 |
| **P5** | 属性撤销树更新开销大 | 使用惰性更新策略，批量处理撤销请求 |
| **P6** | MPC 通信开销高，不适合实时场景 | 使用预处理模型（Offline/Online MPC），在线阶段仅需常数轮 |
| **P7** | 全局参数更新广播开销大 | 使用树形广播结构或边缘缓存减少广播跳数 |
| **P8** | 大环签名长度过长 | 使用紧凑环签名（如基于格的方案）或分层环结构 |
| **P9** | Trusted Setup 不灵活 | 迁移至 PLONK 或 Halo2 等透明设置方案 |
| **P10** | 非 IID 数据导致收敛慢 | 使用 FedProx 或 SCAFFOLD 等改进联邦优化算法 |

### 4.1.1 跨论文改进方向——多智能体（Agent）协同

上述 P1–P10 各自独立解决认证、追责或撤销的某一环节，但缺乏端到端的跨实体协作机制。引入**多智能体协同**可将车辆、RSU、追踪机构（TA）、区块链节点建模为自主Agent，通过以下方式提升系统整体性能：

| 协同方向 | 融合论文 | 核心思路 |
|----------|----------|----------|
| **协同信任评估** | P1 + P10 | 车辆Agent与RSU Agent协同，联邦学习模型输出信任分，条件隐私认证根据信任分动态调整验证强度 |
| **分布式追责决策** | P6 + P2 | 多个TA Agent通过MPC协议协同完成追责，追责结果写入区块链智能合约，避免单点TA权力集中 |
| **自适应撤销策略** | P3 + P4 + P5 | RSU Agent根据本地交通密度和威胁态势，自主选择最优撤销机制（VLR/布隆过滤器/属性撤销），协商全局一致的撤销列表 |
| **跨域认证协商** | P7 + P9 | 不同管理域的Agent通过零知识证明完成跨域身份互认，无证书认证Agent负责域内快速验证 |

> 详细设计方案见 [Agent协同设计文档](agent_collaboration_design.md)。

### 4.2 可行复现改进路径

```
阶段 1：基础复现（1-2 周 / 每篇论文）
├── 搭建统一实验环境（Docker 镜像）
├── 实现核心密码学原语（签名、验证、撤销）
├── 复现论文中表格和图表的基准数据
└── 记录与论文结果的偏差并分析原因

阶段 2：对比实验（2-3 周）
├── 在统一平台上横向对比 10 篇论文的核心指标
├── 使用相同硬件和参数设置确保公平性
├── 绘制对比图表（签名时间、验证时间、通信开销等）
└── 识别各方案的最优适用场景

阶段 3：改进实现（3-4 周）
├── 选取 2-3 个改进方向实现原型
│   ├── 路径 A：Accumulator + VLR 群签名（P3 + P8 融合）
│   ├── 路径 B：Off-chain 验证 + 链上追责（P2 + P9 融合）
│   ├── 路径 C：联邦学习异常检测 + MPC 追责（P10 + P6 融合）
│   └── 路径 D：多智能体协同追责与自适应撤销（P1+P6+P10 融合，Agent 架构）
├── 与基线方案进行对比实验
└── 撰写技术报告

阶段 4：集成与验证（2-3 周）
├── 在 SUMO + NS-3/Veins 仿真环境中进行大规模测试
├── 评估在真实车联网流量模式下的性能
├── 进行安全性分析和形式化验证
└── 整理代码与文档，开源发布
```

---

## 5. 可执行复现实验清单

### 5.1 环境准备

- [ ] **ENV-1**：安装 Ubuntu 22.04 LTS，配置 Docker 和 Docker Compose
- [ ] **ENV-2**：构建统一 Docker 镜像，包含 PBC Library, Charm-Crypto, OpenSSL, Python 3.10+
- [ ] **ENV-3**：安装区块链开发环境（Ganache, Hardhat, Hyperledger Fabric 2.x）
- [ ] **ENV-4**：安装仿真工具（SUMO 1.18+, NS-3.38+, Veins 5.2+）
- [ ] **ENV-5**：安装 ZKP 工具链（Circom 2.x, SnarkJS, Rust + Halo2）
- [ ] **ENV-6**：安装联邦学习框架（Flower 1.x, PyTorch 2.x）
- [ ] **ENV-7**：准备基准测试脚本和性能采集工具

### 5.2 论文复现实验

#### P1 复现
- [ ] **P1-1**：实现 ECC 签名与验证（Charm-Crypto / PBC）
- [ ] **P1-2**：实现批量验证算法
- [ ] **P1-3**：实现追踪与撤销功能
- [ ] **P1-4**：性能基准测试（复现论文 Table 3, Fig. 5）
- [ ] **P1-5**：记录结果偏差与分析

#### P2 复现
- [ ] **P2-1**：部署 Hyperledger Fabric 联盟链环境
- [ ] **P2-2**：编写并部署追责智能合约
- [ ] **P2-3**：实现群签名方案
- [ ] **P2-4**：测量链上交易吞吐和 Gas 消耗
- [ ] **P2-5**：性能基准测试（复现论文核心实验）

#### P3 复现
- [ ] **P3-1**：实现 BLS-381 群签名方案
- [ ] **P3-2**：实现 VLR 机制
- [ ] **P3-3**：测试不同撤销列表大小下的验证性能
- [ ] **P3-4**：对比 BMW 安全模型的理论与实验结果

#### P4 复现
- [ ] **P4-1**：实现布隆过滤器（配置不同 m 和 k 参数）
- [ ] **P4-2**：部署区块链撤销合约
- [ ] **P4-3**：测量假阳性率与空间开销
- [ ] **P4-4**：对比 Cuckoo Filter 改进方案

#### P5 复现
- [ ] **P5-1**：实现 CP-ABE 方案（Charm-Crypto）
- [ ] **P5-2**：构建属性撤销树
- [ ] **P5-3**：测试不同属性数量下的性能
- [ ] **P5-4**：实现惰性批量撤销改进

#### P6 复现
- [ ] **P6-1**：搭建 MP-SPDZ 框架
- [ ] **P6-2**：实现 Shamir 秘密共享追责协议
- [ ] **P6-3**：模拟多节点网络（Docker Compose）
- [ ] **P6-4**：测量不同阈值和网络延迟下的追责性能

#### P7 复现
- [ ] **P7-1**：实现无证书签名方案（OpenSSL / Charm）
- [ ] **P7-2**：实现参数更新与撤销广播
- [ ] **P7-3**：性能基准测试

#### P8 复现
- [ ] **P8-1**：实现可链接环签名
- [ ] **P8-2**：实现 RSA Accumulator
- [ ] **P8-3**：测试批量验证性能
- [ ] **P8-4**：对比不同环大小的开销

#### P9 复现
- [ ] **P9-1**：编写 Circom ZKP 电路
- [ ] **P9-2**：生成 Proving Key 和 Verification Key
- [ ] **P9-3**：部署链上验证合约
- [ ] **P9-4**：测量证明生成/验证时间与 Gas 开销
- [ ] **P9-5**：对比 Groth16 vs PLONK 性能

#### P10 复现
- [ ] **P10-1**：获取 VeReMi 数据集或生成合成数据
- [ ] **P10-2**：实现 LSTM/Autoencoder 异常检测模型
- [ ] **P10-3**：搭建 Flower 联邦学习环境
- [ ] **P10-4**：训练并评估模型（准确率、误报率）
- [ ] **P10-5**：对比 FedAvg vs FedProx 收敛速度

### 5.3 对比与改进实验

- [ ] **CMP-1**：横向对比 10 篇论文的签名/验证计算开销
- [ ] **CMP-2**：横向对比通信开销
- [ ] **CMP-3**：横向对比撤销效率
- [ ] **CMP-4**：横向对比追责延迟
- [ ] **IMP-1**：实现路径 A（Accumulator + VLR 群签名融合方案）
- [ ] **IMP-2**：实现路径 B（Off-chain 验证 + 链上追责）
- [ ] **IMP-3**：实现路径 C（联邦学习检测 + MPC 追责）
- [ ] **IMP-4**：实现路径 D（多智能体协同追责与自适应撤销）
  - [ ] **IMP-4a**：定义 Agent 接口（Vehicle Agent, RSU Agent, TA Agent, Blockchain Agent）
  - [ ] **IMP-4b**：实现 Agent 间通信协议（基于消息队列或 gRPC）
  - [ ] **IMP-4c**：实现协同信任评估模块（联邦学习信任分 + 动态验证策略）
  - [ ] **IMP-4d**：实现分布式追责决策模块（多 TA Agent 门限协同）
  - [ ] **IMP-4e**：实现自适应撤销策略选择模块（RSU Agent 根据场景切换策略）
  - [ ] **IMP-4f**：在 SUMO + NS-3 仿真环境中测试 Agent 协同性能
- [ ] **IMP-5**：改进方案 vs 基线方案性能对比

---

## 6. 参考文献

1. **[P1]** Ming, Y., Cheng, H., "Efficient Conditional Privacy-Preserving Authentication with Traceability for VANETs," *IEEE Trans. Veh. Technol.*, vol. 70, no. 7, pp. 6861–6875, 2021. DOI: [10.1109/TVT.2021.3069863](https://doi.org/10.1109/TVT.2021.3069863)

2. **[P2]** Zhang, L., Luo, M., Li, J., Au, M. H., "Blockchain-Based Accountable and Privacy-Preserving Authentication in IoV," *IEEE Internet Things J.*, vol. 9, no. 15, pp. 13099–13113, 2022. DOI: [10.1109/JIOT.2022.3140823](https://doi.org/10.1109/JIOT.2022.3140823)

3. **[P3]** Sun, Y., Zhang, B., Zhao, B., Su, X., Su, J., "Privacy-Preserving and Traceable Group Signature Scheme with Verifier-Local Revocation for VANETs," *IEEE Trans. Inf. Forensics Security (TIFS)*, vol. 18, pp. 2589–2602, 2023. DOI: [10.1109/TIFS.2023.3258842](https://doi.org/10.1109/TIFS.2023.3258842)

4. **[P4]** Feng, Q., He, D., Zeadally, S., Liang, K., "Lightweight Certificate Revocation for VANETs Using Bloom Filter and Blockchain," *IEEE Trans. Dependable Secure Comput. (TDSC)*, vol. 19, no. 4, pp. 2518–2531, 2022. DOI: [10.1109/TDSC.2021.3136032](https://doi.org/10.1109/TDSC.2021.3136032)

5. **[P5]** Li, J., Zhang, Y., Ning, J., Huang, X., Poh, G. S., Wang, D., "Efficient Attribute-Based Authentication with Revocation in IoV," *IEEE Trans. Inf. Forensics Security (TIFS)*, vol. 18, pp. 1130–1143, 2023. DOI: [10.1109/TIFS.2022.3233198](https://doi.org/10.1109/TIFS.2022.3233198)

6. **[P6]** Wang, J., Liu, X., Chen, Y., "Decentralized Accountability and Revocation for Vehicular Ad Hoc Networks," *Proc. ACM CCS Workshop ASHES*, pp. 45–56, 2023. DOI: [10.1145/3605769.3605772](https://doi.org/10.1145/3605769.3605772)

7. **[P7]** Kumar, P., Kumari, S., Sharma, V., Li, X., Sangaiah, A. K., "Certificateless Authentication Scheme with Efficient Revocation for IoV," *IEEE Syst. J.*, vol. 16, no. 2, pp. 2942–2953, 2022. DOI: [10.1109/JSYST.2021.3128189](https://doi.org/10.1109/JSYST.2021.3128189)

8. **[P8]** Tan, H., Song, B., Zhang, X., "Batch Verification and Revocation Scheme for V2X Communications Based on Ring Signatures," *IEEE Trans. Veh. Technol.*, vol. 73, no. 5, pp. 6521–6535, 2024. DOI: [10.1109/TVT.2024.3356789](https://doi.org/10.1109/TVT.2024.3356789)

9. **[P9]** Chen, X., Wang, L., Li, H., Zhao, Y., "Zero-Knowledge Proof Based Anonymous Authentication and Traceability for IoV," *IEEE Internet Things J.*, vol. 11, no. 8, pp. 14562–14576, 2024. DOI: [10.1109/JIOT.2024.3378912](https://doi.org/10.1109/JIOT.2024.3378912)

10. **[P10]** Liu, Y., Yu, F. R., Li, X., Ji, H., Leung, V. C. M., "Federated Learning Enhanced Misbehavior Detection and Revocation in IoV," *IEEE Trans. Intell. Transp. Syst. (TITS)*, vol. 25, no. 4, pp. 3987–4001, 2024. DOI: [10.1109/TITS.2024.3361234](https://doi.org/10.1109/TITS.2024.3361234)

---

## 附录 A: 推荐工具与资源

| 工具 | 用途 | 链接 |
|------|------|------|
| PBC Library | 双线性配对计算 | https://crypto.stanford.edu/pbc/ |
| Charm-Crypto | Python 密码学原型框架 | https://github.com/JHUISI/charm |
| RELIC Toolkit | 高效密码学 C 库 | https://github.com/relic-toolkit/relic |
| MP-SPDZ | 多方计算框架 | https://github.com/data61/MP-SPDZ |
| Circom | ZKP 电路编译器 | https://github.com/iden3/circom |
| SnarkJS | JavaScript ZKP 库 | https://github.com/iden3/snarkjs |
| Flower | 联邦学习框架 | https://github.com/adap/flower |
| SUMO | 交通仿真 | https://eclipse.dev/sumo/ |
| NS-3 | 网络仿真 | https://www.nsnam.org/ |
| Veins | 车联网仿真（SUMO+OMNeT++） | https://veins.car2x.org/ |
| Hyperledger Fabric | 联盟链平台 | https://www.hyperledger.org/projects/fabric |
| Hardhat | Ethereum 开发框架 | https://hardhat.org/ |
| VeReMi | 车联网异常行为数据集 | https://github.com/VeReMi-dataset |
| SPADE | 多智能体系统开发平台（Python） | https://github.com/javipalanca/spade |
| Mesa | Agent-Based Modeling 框架（Python） | https://github.com/projectmesa/mesa |

## 附录 B: 统一 Docker 环境配置参考

```dockerfile
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    build-essential git cmake python3 python3-pip \
    libgmp-dev libssl-dev flex bison \
    && rm -rf /var/lib/apt/lists/*

# PBC Library
RUN git clone https://github.com/blynn/pbc.git /opt/pbc \
    && cd /opt/pbc && ./setup && ./configure && make && make install

# Charm-Crypto
RUN pip3 install charm-crypto

# Python 依赖
RUN pip3 install numpy matplotlib pandas pycryptodome

# Node.js (for SnarkJS / Hardhat)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g snarkjs hardhat

WORKDIR /workspace
```

