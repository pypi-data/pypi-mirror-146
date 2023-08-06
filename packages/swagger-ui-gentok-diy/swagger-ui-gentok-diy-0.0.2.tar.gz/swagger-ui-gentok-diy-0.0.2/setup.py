from setuptools import setup, find_packages

setup(name='swagger-ui-gentok-diy', # 패키지 명

version='0.0.2',

description='Swagger DIY for gentok',

author='KDH',

author_email='dongha0144@naver.com',

license='MIT', # MIT에서 정한 표준 라이센스 따른다

py_modules=['swagger_ui_gentok'], # 패키지에 포함되는 모듈

python_requires='>=3',

install_requires=[], # 패키지 사용을 위해 필요한 추가 설치 패키지

packages=find_packages(exclude=['swagger_ui_gentok_etc']),


)