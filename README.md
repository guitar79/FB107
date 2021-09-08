# FB107

# anaconda environment
conda create -n FB107_Python_env python=3.8
conda env list

# activate 가상환경 시작
mac/linux
conda activate FB107_Python_env

windows
activate FB107_Python_env

# deactivate 가상환경 종료
mac/linux
conda deactivate

windows
deactivate

# install module
conda install
conda install -c conda-forge


# 가상환경 내보내기 (export)
conda env export > FB107_Python_env.yaml

# .yaml 파일로 새로운 가상환경 만들기
conda env create -f FB107_python_env.yaml

# 가상환경 리스트 출력
conda env list

# 가상환경 제거하기
conda env remove -n FB107_Python_env
