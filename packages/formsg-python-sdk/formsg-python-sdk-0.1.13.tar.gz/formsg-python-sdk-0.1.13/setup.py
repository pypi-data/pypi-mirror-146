# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['formsg', 'formsg.schemas', 'formsg.util']

package_data = \
{'': ['*']}

install_requires = \
['PyNaCl>=1.5.0,<2.0.0', 'pytest>=6.2.5,<7.0.0', 'requests>=2.27.1,<3.0.0']

extras_require = \
{':python_version < "3.11"': ['typing_extensions>=4.0.0,<5.0.0']}

setup_kwargs = {
    'name': 'formsg-python-sdk',
    'version': '0.1.13',
    'description': 'Python SDK for FormSG',
    'long_description': '# formsg-python-sdk\nThis is the Python version of the [Form Javascript SDK](https://github.com/opengovsg/formsg-javascript-sdk/), which provides utility functions for verifying FormSG webhooks, as well as decrypting form submissions.\n\nNote that this library is still in beta. \n\n## Requirements\nPython 3.6+\n## Quickstart\n`pip install formsg-python-sdk`\n```python\nimport formsg\n# accepts STAGING or PRODUCTION, determines whether to use staging or production public signing keys\nsdk = formsg.FormSdk("PRODUCTION")\n\n# Your form\'s secret key downloaded from FormSG upon form creation\nFORM_SECRET_KEY = "YOUR-SECRET-KEY"\n\n# This is where your domain is hosted, and should match\n# the URI supplied to FormSG in the form dashboard\nYOUR_WEBHOOK_URI = "your-webhoook-uri"\n\n# decryption without attachments\n# if `verifiedContent` exists as a key in `encrypted_payload`, the return object will include a verified key\ndecrypted = sdk.crypto.decrypt(FORM_SECRET_KEY, encrypted_payload)\n\n# webhook authentication\nHEADER_RESP = "req.header.\'x-formsg-signature\'"\nsdk.webhooks.authenticate(header=HEADER_RESP, uri=YOUR_WEBHOOK_URI)\n\n# decryption with attachments\ndecrypted_with_attachments = sdk.crypto.decrypt_attachments(FORM_SECRET_KEY, encrypted_payload)\n```\n\nRefer to the [example app](https://github.com/opengovsg/formsg-python-sdk/blob/develop/example_app/flask.py) if you\'re running a flask server.\n\n## End-to-end Encryption\n### Format of Submission Response\n\n| Key                    | Type                   | Description                                                                                              |\n| ---------------------- | ---------------------- | -------------------------------------------------------------------------------------------------------- |\n| formId                 | str                 | Unique form identifier.                                                                                  |\n| submissionId           | str                 | Unique response identifier, displayed as \'Response ID\' to form respondents                               |\n| encryptedContent       | str                 | The encrypted submission in base64.                                                                      |\n| created                | str                 | Creation timestamp.                                                                                      |\n| attachmentDownloadUrls | Mapping[str, str] | (Optional) Records containing field IDs and URLs where encrypted uploaded attachments can be downloaded. |\n\n### Format of Decrypted Submissions\n\n`crypto.decrypt(form_secret_key: str, decrypt_params: DecryptParams)`\ntakes in `decrypt_params` as the second argument, and returns an an object with\nthe shape\n\n<pre>\n{\n  responses: FormField[]\n  verified?: NotRequired[Mapping[str, Any]]\n}\n</pre>\n\nThe `decryptParams.encryptedContent` field decrypts into a list of `FormField` objects, which will be assigned to the `responses` key of the returned object.\n\nFurthermore, if `decryptParams.verifiedContent` exists, the function will\ndecrypt and open the signed decrypted content with the package\'s own\n`signingPublicKey` in\n[`constants.py`](https://github.com/opengovsg/formsg-python-sdk/blob/develop/formsg/constants.py).\nThe resulting decrypted verifiedContent will be assigned to the `verified` key\nof the returned object.\n\n> **NOTE** <br>\n> If any errors occur, either from the failure to decrypt either `encryptedContent` or `verifiedContent`, or the failure to authenticate the decrypted signed message in `verifiedContent`, `None` will be returned.\n\nNote that due to end-to-end encryption, FormSG servers are unable to verify the data format.\n\nHowever, the `decrypt` function exposed by this library [validates](https://github.com/opengovsg/formsg-python-sdk/blob/develop/formsg/util/validate.py) the decrypted content and will **return `None` if the\ndecrypted content does not fit the schema displayed below.**\n\n| Key         | Type     | Description                                                                                              |\n| ----------- | -------- | -------------------------------------------------------------------------------------------------------- |\n| question    | str   | The question listed on the form                                                                          |\n| answer      | str   | The submitter\'s answer to the question on form. Either this key or `answerArray` must exist.             |\n| answerArray | List[str] | The submitter\'s answer to the question on form. Either this key or `answer` must exist.                  |\n| fieldType   | str   | The type of field for the question.                                                                      |\n| \\_id        | str   | A unique identifier of the form field. WARNING: Changes when new fields are created/removed in the form. |\n\nThe full schema can be viewed in\n[`validate.ts`](https://github.com/opengovsg/formsg-javascript-sdk/tree/master/src/util/validate.ts).\n\nIf the decrypted content is the correct shape, then:\n\n1. the decrypted content (from `decryptParams.encryptedContent`) will be set as the value of the `responses` key.\n2. if `decryptParams.verifiedContent` exists, then an attempt to\n   decrypted the verified content will be called, and the result set as the\n   value of `verified` key. There is no shape validation for the decrypted\n   verified content. **If the verification fails, `None` is returned, even if\n   `decryptParams.encryptedContent` was successfully decrypted.**',
    'author': 'Chin Ying',
    'author_email': 'chinying@open.gov.sg',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
