# ScyolHelper

 It is automatically completed every Monday at 1 pm, and the screenshot and video link are pushed through Pushplus’s WeChat public account.

>  Pushplus has crashed a lot recently. Server sauce WeChat push or enterprise WeChat notification functions will be added later.

## Getting started

1. [Fork this repository](https://github.com/yanyaoli/ScyolHelper)
2. Select the forked repository -> Settings -> Secrets and Variables -> Action -> New repository secret, add the following secrets variable:

   - Token [Required]: You need to capture the packet and find any request sent to https://dxx.scyol.com/api/*. The required token will be in the request header.

   - Pushplus_token: Apply on the official website of [Pushplus](https://pushplus.hxtrip.com/) to get a free WeChat message push token.

## Features

 You can log in to the mini program using a phone number and password, but the logic for obtaining the openid has not been implemented.

## Demo

<img src="https://github.com/yanyaoli/ScyolHelper/assets/120553430/4b3f7a51-c7ca-4629-8f2c-dd7d919e32aa" height="500" width="300" />
