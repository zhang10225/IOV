# GLOBECOM导向：车联网追责与撤销（2022–2026）可复现论文短名单

> 说明：本清单基于仓库已有文献综述中给出的论文元数据与实验信息进行二次筛选，目标是服务 IEEE GLOBECOM（CISS/IoT）投稿的工程化复现实验与创新拓展。

## 1) 入选论文（5篇，覆盖多技术路线）

### [A] Blockchain-Based Accountable Privacy-Preserving Authentication in IoV
- 作者：Zhang L., Luo M., Li J., Au M. H.
- 年份/来源：2022, IEEE Internet of Things Journal
- DOI：10.1109/JIOT.2022.3140823
- 技术路线：分布式账本 + 可追责匿名认证 + 撤销上链
- 追责/撤销创新点：
  - 通过群签名可链接标签支持事后追责；
  - 利用智能合约触发并记录身份撤销，形成不可篡改审计轨迹。
- 可复现关键点：
  - 工具：Hyperledger Fabric 或 Ethereum + Solidity；
  - 对比方案：传统CRL广播、中心化TA撤销；
  - 指标：追责延迟、撤销传播时延、链上开销（Gas/TPS）。

### [B] Traceable Group Signature Scheme with Verifier-Local Revocation for VANETs
- 作者：Sun Y., Zhang B., Zhao B., Su X., Su J.
- 年份/来源：2023, IEEE TIFS
- DOI：10.1109/TIFS.2023.3258842
- 技术路线：可追踪群签名 + Verifier-Local Revocation (VLR)
- 追责/撤销创新点：
  - 群管理员可打开签名恢复真实身份（追责）；
  - 验证端本地撤销，降低中心化CRL依赖。
- 可复现关键点：
  - 工具：Charm-Crypto/RELIC（BLS曲线参数）；
  - 参数：群成员规模、撤销列表长度、批验证大小；
  - 指标：签名/验证耗时、撤销验证开销、通信负载。

### [C] Lightweight Certificate Revocation for VANETs Using Bloom Filter and Blockchain
- 作者：Feng Q., He D., Zeadally S., Liang K.
- 年份/来源：2022, IEEE TDSC
- DOI：10.1109/TDSC.2021.3136032
- 技术路线：Bloom Filter压缩CRL + 区块链一致性存储
- 追责/撤销创新点：
  - 将大规模CRL压缩成布隆过滤器以减少广播开销；
  - 撤销记录上链，增强审计可追溯和抗篡改。
- 可复现关键点：
  - 工具：Python(bitarray/mmh3) + Ganache/Hardhat；
  - 参数：布隆过滤器位数组长度、哈希函数个数、CRL规模；
  - 指标：误判率(FPR)、传播时延、带宽节省率。

### [D] Attribute-Based Authentication with Revocation in IoV
- 作者：Li J., Zhang Y., Ning J., Huang X., Poh G. S., Wang D.
- 年份/来源：2023, IEEE TIFS
- DOI：10.1109/TIFS.2022.3233198
- 技术路线：CP-ABE/属性认证 + 属性级撤销
- 追责/撤销创新点：
  - 在细粒度访问控制下支持属性撤销；
  - 适合跨域V2X服务中的权限追责链路。
- 可复现关键点：
  - 工具：Charm-Crypto + PBC；
  - 参数：属性数量、策略深度、撤销频次；
  - 指标：密钥更新成本、解密成功率、撤销生效时间。

### [E] Federated Learning Enhanced Misbehavior Detection and Revocation in IoV
- 作者：Liu Y., Yu F. R., Li X., Ji H., Leung V. C. M.
- 年份/来源：2024, IEEE TITS
- DOI：10.1109/TITS.2024.3361234
- 技术路线：联邦学习辅助异常检测 + 撤销闭环
- 追责/撤销创新点：
  - 以检测模型驱动追责触发；
  - 支持“检测→证据聚合→撤销执行”链路联动。
- 可复现关键点：
  - 工具：Flower/PySyft + PyTorch + SUMO/NS-3耦合；
  - 参数：客户端数量、本地训练轮次、非IID强度；
  - 指标：检测准确率/召回率、误撤销率、撤销触发时延。

---

## 2) 面向 GLOBECOM 的 Agent 协同拓展思路

### 思路1：多Agent分层协作的“追责-撤销闭环优化”
- 设计：Vehicle Agent（本地证据）、RSU Agent（区域融合与策略选择）、TA Agent（门限追责）、Blockchain Agent（审计与撤销同步）。
- 创新点：
  1. 将[B]的VLR与[C]的Bloom-CRL做**情境自适应切换**（高密度路段用Bloom-CRL，低时延场景用VLR）；
  2. TA Agent采用k-of-n门限决策，减少单点误撤销风险；
  3. 将[A]上链审计用于事后可验证追责。
- 解决痛点：撤销延迟高、拓扑快速变化下策略僵化、中心化追责瓶颈。

### 思路2：MARL驱动的“最小开销撤销策略编排”
- 设计：RSU Agent使用多智能体强化学习（如MAPPO/QMIX）学习撤销策略动作集合：
  - 动作：{VLR校验, Bloom广播, 局部黑名单, 全局上链撤销}
  - 状态：{车流密度、链路负载、RL长度、攻击告警等级}
  - 奖励：低时延 + 低误撤销 + 低通信开销。
- 与现有论文结合：
  - [C]提供压缩CRL基线；
  - [B]提供VLR基线；
  - [E]提供异常检测触发信号；
  - [A]提供审计一致性。
- GLOBECOM契合点：通信开销可量化、端边云协同可实现、AI+安全融合明确。

---

## 3) 两条可直接落地的投稿实验建议（GLOBECOM风格）

1. **对比维度建议（必须含工程指标）**
   - 基线：单一VLR、单一Bloom-CRL、中心化TA撤销、区块链固定写链策略；
   - 你的方案：Agent协同自适应撤销。
   - 指标：撤销传播95分位时延、追责完成率、误撤销率、每条消息额外字节、RSU CPU占用、链上写入吞吐。

2. **实验平台建议（强调可复现）**
   - 交通/网络：SUMO + NS-3/Veins；
   - 密码原型：Charm-Crypto（群签名/ABE）+ Python原型；
   - 区块链：Fabric测试网（固定节点数/区块间隔）；
   - Agent模块：Ray RLlib 或 PettingZoo + PyTorch；
   - 复现产物：公开配置文件（道路拓扑、车流seed、攻击脚本、合约参数）+ 一键脚本。
