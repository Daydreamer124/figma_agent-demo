# 增强版用户流程图

## 📝 用户流程描述

从「Dark Sign In - Number」的「Mobile/Component/Sing In - Sing Up Switcher」(INSTANCE)跳转到「Dark Sing Up - Number」
从「Dark Sign In - Number」的「Sing In with Email」(TEXT)跳转到「Dark Sign In - Email」
从「Dark Sign In - Email」的「Mobile/Component/Sing In - Sing Up Switcher」(INSTANCE)跳转到「Dark Sing Up - Email」
从「Dark Sign In - Email」的「Sing In with Phone Number」(TEXT)跳转到「Dark Sign In - Number」
从「Dark Sing Up - Number」的「Mobile/Component/Sing In - Sing Up Switcher」(INSTANCE)跳转到「Dark Sign In - Number」
从「Dark Sing Up - Number」的「Sing In with Email」(TEXT)跳转到「Dark Sing Up - Email」
从「Dark Sing Up - Number」的「Input」(FRAME)跳转到「Dark Confirm phone number - filled」
从「Dark Sing Up - Email」的「Mobile/Component/Sing In - Sing Up Switcher」(INSTANCE)跳转到「Dark Sign In - Email」
从「Dark Sing Up - Email」的「Sing In with Phone Number」(TEXT)跳转到「Dark Sing Up - Number」
从「Dark Sing Up - Email」的「state-layer」(FRAME)跳转到「Dark Account Setup 1」
从「Dark Registration Screen」的「state-layer」(FRAME)跳转到「Dark Sign In - Email」
从「Dark Registration Screen」的「state-layer」(FRAME)跳转到「Dark Sing Up - Email」
从「Dark Welcome Screen」的「Mobile/Primary」(INSTANCE)跳转到「Trade Market Dark」
从「Dark Pin setup - filled」的「Long Arrow」(INSTANCE)跳转到「Dark Welcome Screen」
从「Dark Confirm phone number - filled」的「Mobile/Primary」(INSTANCE)跳转到「Dark Pin setup - filled」
从「Dark Account Setup 1」的「Mobile/Primary」(INSTANCE)跳转到「Dark Pin setup - filled」
从「Trade Market Dark」的「Frame 36939」(FRAME)跳转到「Trade Services Light」

## 📊 Mermaid 流程图

```mermaid
graph TD
  Dark_Sign_In___Number["Dark Sign In - Number"] -->|Mobile/Component/Sing In - Sing Up Switcher| Dark_Sing_Up___Number["Dark Sing Up - Number"]
  Dark_Sign_In___Number["Dark Sign In - Number"] -->|Sing In with Email| Dark_Sign_In___Email["Dark Sign In - Email"]
  Dark_Sign_In___Email["Dark Sign In - Email"] -->|Mobile/Component/Sing In - Sing Up Switcher| Dark_Sing_Up___Email["Dark Sing Up - Email"]
  Dark_Sign_In___Email["Dark Sign In - Email"] -->|Sing In with Phone Number| Dark_Sign_In___Number["Dark Sign In - Number"]
  Dark_Sing_Up___Number["Dark Sing Up - Number"] -->|Mobile/Component/Sing In - Sing Up Switcher| Dark_Sign_In___Number["Dark Sign In - Number"]
  Dark_Sing_Up___Number["Dark Sing Up - Number"] -->|Sing In with Email| Dark_Sing_Up___Email["Dark Sing Up - Email"]
  Dark_Sing_Up___Number["Dark Sing Up - Number"] -->|Input| Dark_Confirm_phone_number___filled["Dark Confirm phone number - filled"]
  Dark_Sing_Up___Email["Dark Sing Up - Email"] -->|Mobile/Component/Sing In - Sing Up Switcher| Dark_Sign_In___Email["Dark Sign In - Email"]
  Dark_Sing_Up___Email["Dark Sing Up - Email"] -->|Sing In with Phone Number| Dark_Sing_Up___Number["Dark Sing Up - Number"]
  Dark_Sing_Up___Email["Dark Sing Up - Email"] -->|state-layer| Dark_Account_Setup_1["Dark Account Setup 1"]
  Dark_Registration_Screen["Dark Registration Screen"] -->|state-layer| Dark_Sign_In___Email["Dark Sign In - Email"]
  Dark_Registration_Screen["Dark Registration Screen"] -->|state-layer| Dark_Sing_Up___Email["Dark Sing Up - Email"]
  Dark_Welcome_Screen["Dark Welcome Screen"] -->|Mobile/Primary| Trade_Market_Dark["Trade Market Dark"]
  Dark_Pin_setup___filled["Dark Pin setup - filled"] -->|Long Arrow| Dark_Welcome_Screen["Dark Welcome Screen"]
  Dark_Confirm_phone_number___filled["Dark Confirm phone number - filled"] -->|Mobile/Primary| Dark_Pin_setup___filled["Dark Pin setup - filled"]
  Dark_Account_Setup_1["Dark Account Setup 1"] -->|Mobile/Primary| Dark_Pin_setup___filled["Dark Pin setup - filled"]
  Trade_Market_Dark["Trade Market Dark"] -->|Frame 36939| Trade_Services_Light["Trade Services Light"]
```
