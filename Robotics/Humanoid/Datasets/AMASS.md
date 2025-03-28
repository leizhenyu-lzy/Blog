# AMASS

---

[AMASS : Archive of Motion Capture As Surface Shapes - Website](https://amass.is.tue.mpg.de/)

[AMASS - Github](https://github.com/nghorbani/amass)

[Retargeted AMASS for Robotics - HuggingFace](https://huggingface.co/datasets/fleaven/Retargeted_AMASS_for_robotics)
1. [下载方法](../../../HuggingFace/HuggingFace.md)

---

MoCap = motion capture

main problem
1. current MoCap datasets are small
2. different parameterization(参数化) of body

contribute
1. unify 15 **optical marker-based** MoCap datasets & representing within a common framework and **parameterization**
   1. input : sparse markers
   2. output : SMPL body models
2. **MoSh++** : convert mocap data into realistic 3D human meshes by
   1. Rigged Body Model(绑定身体模型)
      1. 骨骼结构(rig) + 蒙皮(skin)
   2. 控制骨骼关节(joints)




# Installation

[AMASS 官网](https://amass.is.tue.mpg.de/index.html)
1. 注册登录，Download 数据集

[AMASS - Github](https://github.com/nghorbani/amass)
1. 创建一个虚拟环境 & 基础安装
   1. `conda create -n amass python=3.10 -y` + `conda activate amass`
   2. `pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126`
   3. `pip3 install pyrender`
   4. `conda install pytorch3d -c pytorch3d`
   5. `pip install ipykernel`
   6. `pip install matplotlib`
2. clone `amass` 并 `cd` 进入
   1. 修改 `requirements.txt` 删掉所有 版本要求
   2. `pip install -r requirements.txt`
   3. `python setup.py develop`
3. clone `human_body_prior` 并 `cd` 进入
   1. 修改 `requirements.txt` 删掉所有 版本要求 以及 pytorch3d
   2. `pip install -r requirements.txt`
   3. `python setup.py develop`


下载 ``
1. [SMPL - Downloads](https://smpl.is.tue.mpg.de/download.php)
2. 注册登录，找到 **DMPLs for AMASS** -> **Download DMPLs compatible with SMPLlz**





删除环境 `conda remove -n amass --all`



