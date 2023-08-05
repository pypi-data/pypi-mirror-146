# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lk_qtquick_scaffold',
 'lk_qtquick_scaffold.experimental_features',
 'lk_qtquick_scaffold.pyside',
 'lk_qtquick_scaffold.qmlside',
 'lk_qtquick_scaffold.qmlside.hot_loader',
 'lk_qtquick_scaffold.qmlside.layout_helper',
 'lk_qtquick_scaffold.qmlside.resource_manager']

package_data = \
{'': ['*'],
 'lk_qtquick_scaffold': ['themes/*',
                         'themes/Theme/*',
                         'themes/Theme/LightClean/*',
                         'themes/Theme/LightClean/LCBackground/*',
                         'themes/Theme/LightClean/LCButtons/*',
                         'themes/Theme/LightClean/LCComplex/*',
                         'themes/Theme/LightClean/LCStyle/*',
                         'themes/Theme/LightClean/rss/*',
                         'themes/Theme/SimpleUI/*']}

install_requires = \
['lk-lambdex', 'lk-logger', 'lk-utils', 'pyside6']

setup_kwargs = {
    'name': 'lk-qtquick-scaffold',
    'version': '1.2.0',
    'description': 'A flexible toolset for improving QML coding experience in PySide6 development.',
    'long_description': '# LK QtQuick Scaffold\n\nUsing Python and Qt QML to build desktop applications from a series of\npredefined tools.\n\n# How to Install\n\n```\npip install lk-qtquick-scaffold\n```\n\n*Python 3.8 is the minimum required version.*\n\n# Highlights\n\n- A layout engine to extend QML layouts.\n- Integrate qt logging with python console (no need to enable "emulate terminal\n  in output console" in PyCharm).\n- Executing Python snippet in QML, and vice versa.\n- Easy-to-use register handler for registering Python functions to QML side.\n- Hot loader for testing target layout.\n- Assets manager to thoroughly control application appearance (color, motion,\n  shape, typograph, and so on).\n- A built-in theme to quickly produce elegant user interface. For example,\n  use `LCButton` or `LCGhostButton` to replace the normal `Button`.\n    - Currently (v1.x) there\'s only one theme (LightClean Theme) provided.\n\n# Feature Quickview\n\n## Layout Engine\n\n```qml\nimport QtQuick\n\nItem {\n    Rectangle {\n        Component.onCompleted: {\n            LKLayoutHelper.quick_anchors(this, parent, {\n                \'reclines\': [1, 1, 0, 1], // left, top, right, bottom\n                \'margins\': [12, 4, 12, 4] // left, top, right, bottom\n            })\n        }\n    }\n}\n```\n\n```qml\nimport QtQuick\n\nRow {\n    spacing: 4\n    \n    Rectangle {\n        width: 0.5 // 50% of parent.width (respect parent.spacing)\n        height: parent.height\n    }\n    \n    Rectangle {\n        width: 0.2 // 20% of parent.width (respect parent.spacing)\n        height: parent.height\n    }\n    \n    Rectangle {\n        width: 0 // fill the rest (30% of parent.width) (respect parent.spacing)\n        height: parent.height\n    }\n    \n    Component.onCompleted: {\n        LKLayoutHelper.hadjust_children_size(this)\n    }\n}\n```\n\n*TODO:MoreExamples*\n\n## Integrate qt logging with python console\n\n![](./.assets/20211024201434.png)\n\n## Executing Python snippet in QML, and vice versa\n\n```python\nfrom lk_qtquick_scaffold import eval_js\n\ndef foo(a: QObject, b: QObject):\n    eval_js(\'\'\'\n        {0}.anchors.left = Qt.binding(() => {{\n            return {1}.anchors.left\n        }})\n    \'\'\', a, b)\n```\n\n```qml\nimport QtQuick\n\nListView {\n    model: pyside.eval(`\n        import os\n        files = os.listdir(input(\'target folder: \'))\n        return files\n    `)\n}\n```\n\n## Register Python functions to QML side\n\nThere\'re two ways to register:\n\n```python\nfrom lk_qtquick_scaffold import reg\n\n@reg()\ndef foo(*args, **kwargs):\n    print(args, kwargs)\n    return True\n```\n\n```python\nfrom lk_qtquick_scaffold import pyside\n\ndef foo(*args, **kwargs):\n    print(args, kwargs)\n    return True\n\npyside.register(foo)\n```\n\nThen call it by function name in QML side:\n\n```qml\nimport QtQuick\n\nItem {\n    Component.onCompleted: {\n        var result = pyside.call(\'foo\', [1, 2, 3], {\'aaa\': 4, \'bbb\': 5})\n    }\n}\n```\n\n## Hot Loader\n\n```python\nfrom lk_qtquick_scaffold import app, hot_loader\n\n# Just replace `app.start` with `hot_loader.start`\n# app.start(\'view.qml\')\nhot_loader.start(\'view.qml\')\n```\n\n![](.assets/20211024203352.png)\n\n## Assets Manager\n\n*TODO:AssetsManagerExample*\n\n## LightClean Theme\n\nSee\nalso [code_examples/eg01_viscous_indicator_anim](code_examples/animations/eg01_viscous_indicator_anim/view.qml):\n\n```qml\nimport QtQuick\nimport LightClean\nimport LightClean.LCComplex\n\nLCWindow {\n    width: 280\n    height: 360\n\n    LCSideBar {\n        anchors.fill: parent\n\n        // icon from: https://iconduck.com/sets/bubblecons-nations-icon-set\n        p_model: [\n            {m_title: \'Sprint\', m_icon: \'file:stopwatch.svg\'},\n            {m_title: \'Boomerang\', m_icon: \'file:boomerang.svg\'},\n            {m_title: \'Football\', m_icon: \'file:football-spain.svg\'},\n        ]\n    }\n}\n```\n\nIn this example, `LCSideBar` uses a simple model struct to generate items. Each\nitem has apperance in different status (hovered, selected, etc.), an indicator\nmoves when selection changed.\n\n![](gallery/widgets_demo/viscous-indicator-anim.gif)\n\n**More screenshots**\n\n![](gallery/widgets_demo/swipe-view.gif)\n\n![](gallery/widgets_demo/breathing-circle-avatar.gif)\n\n![](gallery/widgets_demo/password-eye-open.gif "https://uimovement.com/media/resource_image/image_5213.gif.mp4")\n\n*TODO:AddMoreWidgetsDemo*\n\n# Working in Progress\n\n- The documentation is far away to ready status.\n- LightClean Theme is found in Sept. 2020, but it is under refactoring in recent\n  months.\n    - The documentation is not provided. You have to check its source code for\n      more infomation.\n    - Some old widgets have bugs unfixed.\n- The registered functions by `@reg()` or `pyside.register()` are not Slot\n  functions. So it may cause GUI latency on doing heavy task. (It will be\n  resolved in future releases.)\n',
    'author': 'Likianta',
    'author_email': 'likianta@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
