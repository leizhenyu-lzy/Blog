# 坐标系

[知乎 - 常用坐标系及投影：WGS84\GCJ02\CGCS2000\BD09\Pseudo-Mercator\UTM\BD09MC](https://zhuanlan.zhihu.com/p/363528840)

[知乎 - 中国使用2000坐标系而不使用WGS84坐标系的原因和意义是什么？](https://www.zhihu.com/question/35775670)


分类
1. WGS84\GCJ02\CGCS2000\BD09是地心坐标系，坐标表现形式为经度、纬度
2. Pseudo-Mercator(墨卡托)\UTM\BD09MC是投影坐标系，坐标表现形式为x、y
3. WGS84\CGCS2000是原始坐标系，GCJ02\BD09是加密坐标系

使用情况
1. 谷歌、OSM等地图使用的是WGS84坐标系和Pseudo-Mercator投影坐标系
2. 高德、腾讯等地图使用的是GCJ02坐标系和Pseudo-Mercator投影坐标系
3. 天地图使用的CGCS2000坐标系和Pseudo-Mercator投影坐标系
4. 百度地图使用的是BD09坐标系和BD09MC投影坐标系
5. UTM投影坐标系经常应用在无人驾驶及高精地图上面
6. 国内Android系统手机采集的AGPS数据是GCJ02坐标系的
7. RTK和一些PDA设备采集的GPS数据是WGS84坐标系的
8. IOS系统手机采集的AGPS数据是WGS84坐标系的GPS定位芯片获取的定位数据是WGS84坐标系的
9. 北斗芯片获取的定位数据是CGCS2000坐标系的

CGCS2000坐标系
1. China Geodetic Coordinate System 2000，2000国家大地坐标系
2. 我国当前最新的国家大地坐标系，它的EPSG编码为，4490
3. 正式名称为2000国家大地坐标系，是以国际地球框架ITRF1997为参考，采用2000历元建立的区域性地心坐标系统，于2008年正式启用

WGS84坐标系
1. World Geodetic System-1984，既1984年的全球坐标系统
2. 全球卫星定位系统（GPS）建立的一个全球地心坐标系统，美国GPS系统使用的是WGS84坐标系
3. WGS84是动态维持的坐标系统，几经修正后当前的WGS84（G1674）与ITRF2008在历元2005.0处一致

