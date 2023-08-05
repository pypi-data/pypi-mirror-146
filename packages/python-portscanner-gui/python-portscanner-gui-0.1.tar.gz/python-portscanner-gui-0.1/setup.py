from setuptools import setup

with open("README.md", 'r') as f:
	long_description = f.read()

setup(
	name='python-portscanner-gui',
	version='0.1',
	license="MIT",
	description='A simple graphical portscanner built in Python.',
	long_description=long_description,
	author='Jason O\'Neal',
	author_email='jason.allen.oneal@gmail.com',
	url='https://github.com/jason-allen-oneal/python-portscanner-gui',
	packages=['python-portscanner-gui'],
	install_requires=['scapy'],
	classifiers=[
		'Development Status :: 4 - Beta',
		'Environment :: X11 Applications',
		'Intended Audience :: Developers',
		'Intended Audience :: System Administrators',
		'License :: OSI Approved :: BSD License',
		'Operating System :: POSIX :: Linux',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.7',
		'Topic :: Security',
		'Topic :: Internet',
		'Topic :: System :: Networking',
		'Topic :: Utilities'
	],
)
