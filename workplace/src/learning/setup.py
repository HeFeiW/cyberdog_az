from setuptools import setup

package_name = 'learning'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mi',
    maintainer_email='mi@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'stand = learning.stand:main',
            'sit = learning.sit:main',
            'distance = learning.distance:main',
            'walktest = learning.walktest:main',
            'rgb_cam_suber = learning.rgb_cam_suber:main',
            'infra_cam_suber = learning.infra_cam_suber:main',
            'rgb_test = learning.rgb_test:main',
            'track = learning.track:main',
            'crash = learning.crash:main',
            'data_reciv = learning.data_reciv:main',
            'walk_t_sec = learning.walk_t_sec:main',
            'test = learning.test:main',
            'rotate = learning.rotate:main',
            'data_receive = learning.data_receive:main',
            'striker = learning.striker:main',
            'goal = learning.goal:main',
            'routine = learning.routine:main',
            'moveto = learning.move_to_target:main',
            'shoot = learning.shoot:main'
        ],
    },
)
