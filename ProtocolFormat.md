# 协议格式

## 16口串口服务器
IP: 192.168.1.82

| 总线 | 串口服务器port | IP port |
| :---: | :---: | :---: |
| 空调1 | port1 | 1030|
| 空调2 | port2 | 1031|
| 空调3 | port3 | 1032|
| 空调4 | port4 | 1033|
| 空调5 | port5 | 1034|
| 空调6 | port6 | 1035|
| 空调7 | port7 | 1036|
| 空调8 | port8 | 1037|
| 空调9 | port9 | 1038|
| 环境1 | port10 | 1039|
| 环境2 | port11 | 1040|
| 环境3 | port12 | 1041|
| 环境4 | port13 | 1042|
| 环境5 | port14 | 1043|
| 环境6 | port15 | 1044|


## 8口串口服务器
IP: 192.168.1.83

| 总线 | 串口服务器port | IP port |
| :---: | :---: | :---: |
| 环境7 | port1 | 1030 |
| 环境8 | port2 | 1031 |
| 环境9 | port3 | 1032 |
| 环境10 | port4 | 1033 |
| 环境11 | port5 | 1034 |
| 电表 | port6 | 1035 |
| 主机 | port7 | 1036 |

## 房间电表
IP: 192.168.1.146
port: 12345

## Modbus连接设置
|类型| 波特率| 校验位 | 数据位 | 停止位 |
| :---: | :---: | :---: | :---: | :---: |
| 空调 | 115200 | NONE | 8 | 1 |
| 环境 | 9600 | NONE | 8 | 1 |
| 电表 | 2400 | EVEN | 8 | 1 |
| 主机 | 9600 | NONE | 8 | 1 |
| 房间电表 | 9600 | NONE | 8 | 1 |




## modbus-rtu命令
| 设备地址| 功能码 | 起始地址 | 读寄存器长度 | 校验码 |
| :---: | :---: | :---: | :---: | :---: |
| 0x01 | 0x03 | 0x00 0x00 | 0x00 0x02 | 0xC4 0x0B |



## 环境空气质量传感器

### 指令
| | 设备地址| 功能码 | 起始地址 | 寄存器数量 | 备注 |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 环境质量 | 云盒编号 | 读保持寄存器（0x03） | 0x00 0x00 | 0x00 0x73 | 一条总线上多个云盒，一个云盒上多个传感器 |
| 空调 | 0x01 | 读线圈（0x01） | 0x00 | 0x10 | True/False表示对应传感器是否在线 |
| 空调12345 | 0x01 | 读保持寄存器（0x03） | 传感器编号*0x40（从0开始） | 0x00 0x04 | 一条总线仅有一个设备地址，不同传感器对应不同寄存器位置 |
| 空调6789 | 0x01 | 读保持寄存器（0x03） | 0x00 | 0x10 | 一条总线只读一次数据，不同传感器数据在返回数据中按地址寻址 |
| 电表 | 0x01 | 读保持寄存器（0x03） | 对应地址 | 0x01 | 一个数据对应一个寄存器地址 |
| 主机 | 0x01 | 读保持寄存器（0x03） | 对应地址 | 0x01 | 一个数据对应一个寄存器地址 |

### 数据解析

<!--
## 空调出风传感器

### 指令
| 传感器编号 | 云盒地址 | 功能码 | 起始寄存器 |
|------|------|------|------|
||||

### 数据解析


## 水箱传感器

### 指令
| 传感器编号 | 云盒地址 | 功能码 | 起始寄存器 |
|------|------|------|------|
||||

### 数据解析
-->

## 空调
01: 温度
02: 湿度
30: 风速
81: 压力液位(MPa)
82: 压力液位(Bar)
### 总线1
|| 起始地址| 数据类型 | 含义 |
| :---: | :---: | :---: | :---: |
| 01 | 0x00 0x00 | 0x81 | 冷水箱液位 |
| 02 | 0x00 0x40 | 0x81 | 热水箱液位 |
| 03 | 0x00 0x80 | 0x01 | 热水箱0.30m处温度 |
| 04 | 0x00 0xC0 | 0x01 | 热水箱0.15m处温度 |
| 05 | 0x10 0x00 | 0x01 | 热水箱0.45m处温度 |
| 06 | 0x10 0x40 | 0x01 | 热水箱0.75m处温度 |
| 07 | 0x10 0x80 | 0x01 | 冷水箱0.45m处温度 |
| 08 | 0x10 0xC0 | 0x01 | 冷水箱0.60m处温度 |
| 09 | 0x20 0x00 | 0x01 | 冷水箱0.30m处温度 |
| 10 | 0x20 0x40 | 0x01 | 热水箱0.60m处温度 |
| 11 | 0x20 0x80 | 0x01 | 热水箱0.90m处温度 |
| 12 | 0x20 0xC0 | 0x01 | 冷水箱0.75m处温度 |
| 13 | 0x30 0x00 | 0x01 | 冷水箱0.15m处温度 |
| 14 | 0x30 0x40 | 0x01 | 冷水箱0.90m处温度 |

### 总线2
|| 起始地址| 数据类型 | 含义 |
| :---: | :---: | :---: | :---: |
| 01 | 0x00 0x00 | 0x01 | 1号房间顶上空调进水管温度 |
| 02 | 0x00 0x40 | 0x01 | 1号房间顶上空调回水管温度 |

### 总线3
|| 起始地址| 数据类型 | 含义 |
| :---: | :---: | :---: | :---: |
| 01 | 0x00 0x00 | 0x01 | 3号房间顶上空调进水管温度 |
| 02 | 0x00 0x40 | 0x01 | 3号房间顶上空调回水管温度 |
| 03 | 0x00 0x80 | 0x01 | 4号房间顶上空调进水管温度 |
| 04 | 0x00 0xC0 | 0x01 | 4号房间顶上空调回水管温度 |

### 总线4
|| 起始地址| 数据类型 | 含义 |
| :---: | :---: | :---: | :---: |
| 01 | 0x00 0x00 | 0x82 | 末端供水进水管压力 |
| 02 | 0x00 0x40 | 0x82 | 设备循环泵回水管压力 |
| 03 | 0x00 0x80 | 0x82 | 末端供水回水管压力 |
| 04 | 0x00 0xC0 | 0x82 | 设备循环泵进水管压力 |
| 05 | 0x01 0x00 | 0x82 | 生活热水进水管压力 |
| 06 | 0x01 0x40 | 0x01 | 设备循环泵进水管温度 |
| 07 | 0x01 0x80 | 0x01 | vip室顶上空调回水管温度 |
| 08 | 0x01 0xC0 | 0x01 | 调度室顶上空调进水管温度 |
| 09 | 0x02 0x00 | 0x01 | 调度室顶上空调回水管温度 |
| 10 | 0x02 0x40 | 0x01 | vip室顶上空调进水管温度 |
| 11 | 0x02 0x80 | 0x01 | 末端供水进水管温度 |
| 12 | 0x02 0xC0 | 0x01 | 末端供水回水管温度 |
| 13 | 0x03 0x00 | 0x01 | 生活热水进水管温度 |
| 14 | 0x03 0x40 | 0x01 | 设备循环泵回水管温度 |

### 总线5
|| 起始地址| 数据类型 | 含义 |
| :---: | :---: | :---: | :---: |
| 01 | 0x00 0x00 | 0x01 | 会议室前面顶上空调进水管温度 |
| 02 | 0x00 0x40 | 0x01 | 会议室前面顶上空调回水管温度 |
| 03 | 0x00 0x80 | 0x01 | 会议室后面顶上空调进水管温度 |
| 04 | 0x00 0xC0 | 0x01 | 会议室后面顶上空调回水管温度 |
| 05 | 0x01 0x00 | 0x01 0x02 | 调度室顶上空调出风口温湿度 |

### 总线6
|| 起始地址| 数据类型 | 含义 |
| :---: | :---: | :---: | :---: |
| 01 | 0x00 0x00 | 0x01 | 1号房间空调出风温度 |
| 02 | 0x00 0x40 | 0x02 | 1号房间空调出风湿度 |
| 03 | 0x00 0x80 | 0x30 | 1号房间空调出风风速 |

### 总线7
|| 起始地址| 数据类型 | 含义 |
| :---: | :---: | :---: | :---: |
| 01 | 0x00 0x00 | 0x01 | 3号房间空调出风温度 |
| 02 | 0x00 0x40 | 0x02 | 3号房间空调出风湿度 |
| 03 | 0x00 0x80 | 0x30 | 3号房间空调出风风速 |
| 04 | 0x00 0xC0 | 0x01 | 4号房间空调出风温度 |
| 05 | 0x00 0x00 | 0x02 | 4号房间空调出风湿度 |
| 06 | 0x00 0x80 | 0x30 | 4号房间空调出风风速 |

### 总线8
|| 起始地址| 数据类型 | 含义 |
| :---: | :---: | :---: | :---: |
| 01 | 0x00 0x00 | 0x01 | VIP间空调出风温度 |
| 02 | 0x00 0x40 | 0x02 | VIP间空调出风湿度 |
| 03 | 0x00 0x80 | 0x30 | VIP间空调出风风速 |
XXX| 04 | 0x00 0xC0 | 0x01 | 调度间空调出风温度 |
XXX| 05 | 0x00 0x00 | 0x01 | 调度间空调出风湿度 |

### 总线9
|| 起始地址| 数据类型 | 含义 |
| :---: | :---: | :---: | :---: |
| 01 | 0x00 0x00 | 0x01 | 会议室前面空调出风温度 |
| 02 | 0x00 0x40 | 0x02 | 会议室前面空调出风湿度 |
| 03 | 0x00 0x80 | 0x30 | 会议室前面空调出风风速 |
| 04 | 0x00 0xC0 | 0x01 | 会议室后面空调出风温度 |
| 05 | 0x00 0x00 | 0x02 | 会议室后面空调出风湿度 |
| 06 | 0x00 0x80 | 0x30 | 会议室后面空调出风风速 |

### 电表
|| 寄存器地址| 数据长度 | 含义 | 单位 | 变量 |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 01 | 0x0000 | 2 | 当前组合有功总电能 | 0.01kWh | current_combine_total_active_energy |
| 02 | 0x000A | 2 | 当前正向有功总电能 | 0.01kWh | current_positive_total_active_energy |
| 03 | 0x0014 | 2 | 当前反向有功总电能 | 0.01kWh | current_negative_total_active_energy |
| 04 | 0x0186 | 2 | 当前无功总电能 | 0.01kWh | current_total_useless_energy |
| 05 | 0x0300 | 1 | A相电压 | 0.1V | voltage_A |
| 06 | 0x0301 | 1 | B相电压 | 0.1V | voltage_B |
| 07 | 0x0302 | 1 | C相电压 | 0.1V | voltage_C |
| 08 | 0x0303 | 1 | A相电流 | 0.01A | electric_current_A |
| 09 | 0x0304 | 1 | B相电流 | 0.01A | electric_current_B |
| 10 | 0x0305 | 1 | C相电流 | 0.01A | electric_current_C |
| 11 | 0x0306 | 1 | 瞬时A相有功功率 | 0.01kW | instant_active_power_A |
| 12 | 0x0307 | 1 | 瞬时B相有功功率 | 0.01kW | instant_active_power_B |
| 13 | 0x0308 | 1 | 瞬时C相有功功率 | 0.01kW | instant_active_power_C |
| 14 | 0x0309 | 1 | 瞬时总有功功率 | 0.01kW | instant_total_active_power |
| 15 | 0x030A | 1 | 瞬时A相无功功率 | 0.01kvar | instant_useless_power_A |
| 16 | 0x030B | 1 | 瞬时B相无功功率 | 0.01kvar | instant_useless_power_B |
| 17 | 0x030C | 1 | 瞬时C相无功功率 | 0.01kvar | instant_useless_power_C |
| 18 | 0x030D | 1 | 瞬时总无功功率 | 0.01kvar | instant_useless_total_power |
| 19 | 0x030E | 1 | 瞬时A相视在功率 | 0.01kVA | instant_apparent_power_A |
| 20 | 0x030F | 1 | 瞬时B相视在功率 | 0.01kVA | instant_apparent_power_B |
| 21 | 0x0310 | 1 | 瞬时C相视在功率 | 0.01kVA | instant_apparent_power_C |
| 22 | 0x0311 | 1 | 瞬时总视在功率 | 0.01kVA | instant_apparent_total_power |
| 23 | 0x0312 | 1 | A相功率因素 | 0.001 | power_factor_A |
| 24 | 0x0313 | 1 | B相功率因素 | 0.001 | power_factor_B |
| 25 | 0x0314 | 1 | C相功率因素 | 0.001 | power_factor_C |
| 26 | 0x0315 | 1 | 总功率因素 | 0.001 | power_factor_total |
| 27 | 0x0316 | 1 | 频率 | 0.01Hz | frequency |

### 主机
| | 寄存器地址| 含义 | 单位 | 变量 |
| :---: | :---: | :---: | :---: | :---: |
| 01 | 0 | 模式设定 | - | mode_setting |
| 02 | 1 | 制热温度设定 | 摄氏度 | heating_temperature_setting |
| 03 | 2 | 制冷温度设定 | 摄氏度 | cooling_temperature_setting |
| 04 | 3 | 制热水温度设定 | 摄氏度 | hot_water_temperature_setting |
| 05 | 4 | 水位设定 |      | water_level_setting |
| 06 | 100 | 水箱温度 | 摄氏度 | water_tank_temperature |
| 07 | 101 | 总出水温度 | 摄氏度 | total_outlet_water_temperature |
| 08 | 102 | 机组在线状态（1-在线 0-不在线）| - | equipment_online_status |
| 09 | 3000 | 主控从机地址 |   | master_slave_address |
| 10 | 3001 | 主控从机机型 |   | master_slave_model   |
| 11 | 3002 | 故障低位 |    | fault_low_bit |
| 12 | 3003 | 故障高位 |    | fault_high_bit |
| 13 | 3004 | 主控软件版本 |    | master_control_software_version |
| 14 | 3005 | 运行模式（0-关机 1-水泵 2-制冷 3-制热 4-制热水 5-采暖 6-电加热） | - | operating_mode |
| 15 | 3006 | 运行能需 |  | operating_energy_requirements |
| 16 | 3007 | 总出水温度Tw | 摄氏度 | total_outlet_water_temperature_Tw |
| 17 | 3008 | 单元出水温度 | 摄氏度 | unit_outlet_water_temperature |
| 18 | 3009 | 单元进水温度 | 摄氏度 | unit_inlet_water_temperature |
| 19 | 3010 | 冷凝口出水温度T3A | 摄氏度 | condensate_outlet_water_temperature_T3A |
| 20 | 3011 | 冷凝口出水温度T3B | 摄氏度 | condensate_outlet_water_temperature_T3B |
| 21 | 3012 | 室外环境温度 | 摄氏度 | outdoor_ambient_temperature |
| 22 | 3013 | 水侧防冻温度 | 摄氏度 | waterside_freeze_protection_temperature |
| 23 | 3014 | 板换进口温度T6A | 摄氏度 | plate_change_inlet_temperature_T6A |
| 24 | 3015 | 板换进口温度T6B | 摄氏度 | plate_change_inlet_temperature_T6B |
| 25 | 3016 | 系统回气温度 | 摄氏度 | system_return_air_temperature |
| 26 | 3017 | T2冷媒液侧温度 | 摄氏度 | T2_refrigerant_liquid_side_temperature |
| 27 | 3018 | 总冷出温度Tz | 摄氏度 | total_cold_out_temperature_Tz |
| 28 | 3019 | 回气饱和温度Te | 摄氏度 | return_air_saturation_temperature_Te |
| 29 | 3020 | 排气饱和温度Tc | 摄氏度 | exhaust_air_saturation_temperature_Tc |
| 30 | 3021 | 排气过热度TdSH |      | exhaust_air_superheat_degree_TdSH |
| 31 | 3022 | 回气过热度TsSH |      | return_air_superheat_degree_TsSH |
| 32 | 3023 | 电子膨胀阀EXVA |      | electronic_expansion_valve_EXVA |
| 33 | 3024 | 电子膨胀阀EXVB |      | electronic_expansion_valve_EXVB |
| 34 | 3025 | 电子膨胀阀EXVC |      | electronic_expansion_valve_EXVC |
| 35 | 3026 | 电磁阀SV（BIT0-SV1 BIT1-SV2 BIT2-SV3 BIT3-SV4 BIT4-SV5 BIT5-SV6 BIT6-SV7 BIT7-SV8）|   | solenoid_valve |
| 36 | 3027 | 其他负载（BIT0-ST四通阀 BIT1-Cycpump水泵 BIT2-PanHeat底盘电加热 BIT3-Heat1辅助电加热 BIT4-Heat2靶流电加热 BIT5-FrostHeat防冻加热带 BIT7-Crank压缩机加热带）| | other_loads |
| 37 | 3028 | 风挡1 |    | windscreen_1 |
| 38 | 3029 | 风挡2 |    | windscreen_2 |
| 39 | 3030 | 频率1 |    | frequency_1 |
| 40 | 3031 | 排气温度1 |    | exhaust_air_temperature_1 |
| 41 | 3032 | 散热器温度1 |   | heat_sink_temperature_1 |
| 42 | 3033 | 电流1 |    | current_1 |
| 43 | 3034 | 频率2 |    | frequency_2 |
| 44 | 3035 | 排气温度2 |    | exhaust_air_temperature_2 |
| 45 | 3036 | 散热器温度2 |   | heat_sink_temperature_2 |
| 46 | 3037 | 电流2 |    | current_2 |
| 47 | 3038 | 高压压力 |    | high_pressure |
| 48 | 3039 | 低压压力 |    | low_pressure |

### 房间电表
| 房间 | 通讯地址 |
| :---: | :---: |
| room1 | 24 |
| room2 | 48 |
| room4 | 87 |

| | 寄存器地址| 含义 | 数据长度 | 变量 |
| :---: | :---: | :---: | :---: | :---: |
| 01 | 0x2000 | A相电压 | 2 | voltage |
| 02 | 0x2002 | A相电流 | 2 | electric_current |
| 03 | 0x2004 | 瞬时总有功功率 | 2 | instant_total_active_power |
| 04 | 0x2006 | 瞬时总无功功率 | 2 | instant_useless_total_power |
| 05 | 0x2008 | 瞬时总视在功率 | 2 | instant_apparent_total_power |
| 06 | 0x200A | 总功功率因数 | 2 | power_factor_total |
| 07 | 0x200E | 电网频率 | 2 | grid_frequency |
| 08 | 0x4000 | 有功总电能 | 2 | total_active_energy |



