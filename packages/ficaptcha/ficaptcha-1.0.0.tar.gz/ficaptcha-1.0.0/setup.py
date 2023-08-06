import setuptools

setuptools.setup(
	name="ficaptcha",
	version="1.0.0",
	author="Danil Kononyuk",
	author_email="me@0x7o.link",
	description="Simple captcha",
	long_description="""# fiCaptcha
Module for image-captcha generation

## Build from source
```
git clone https://github.com/0x7o/fiCaptcha
cd fiCaptcha
pip install .
```""",
	long_description_content_type="text/markdown",
	url="https://github.com/0x7o/fiCaptcha",
	packages=setuptools.find_packages(),
	classifiers=[],
	python_requires='>=3.6',
)