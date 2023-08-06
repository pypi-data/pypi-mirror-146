from setuptools import setup

setup(name='aebo_pi',
      version='0.2',
      description='This package is for ABG robot running on a RPI',
      url='http://www.aeroboticsglobal.com/',
      author='Aerobotics Global',
      author_email='lokeshkode@aeroboticsglobal.com',
      license='MIT',
      packages=['aebo_pi'],
      install_requires=[
          'nltk',
          'scikit-learn>=0.24',
          'numpy>=1.21',
          'opencv-contrib-python',
          'lobe',
          'mediapipe-rpi4',
          
      ],
      zip_safe=False)
