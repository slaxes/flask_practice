# Beibei Test


**以下接口`Content Type`均为`application/json`**

### HTTP Method

```
[POST]
```

### Path

```
/info
```

### Post Body参数

示例

```JSON
{
    "id": 2,
    "main-question1": 1,
    "main-question2": 2,
}
```

字段说明

|字段|类型|说明|样例|是否必需|
|:---:|:---:|:---:|:---:|:---:|
|id|int|每个query的唯一标志|1|是|
|main-question1|int|1:正确，2:错误，3:未知|2|是|
|main-question2|int|1:正确，2:错误，3:未知|1|是|

### Get参数

样例
```JSON
{
  "result": [
    {
      "query": 你好，
      "main-question1": 你好，
      "main-question1": 你好，
      "id": 1
    }
  ]
}
```

字段说明

|字段|类型|说明|样例|是否必需|
|:---:|:---:|:---:|:---:|:---:|
|query|string|用户问题|你好|是|
|main-question1|string|模型1预测的主问题|你好|是|
|main-question2|string|模型2预测的主问题|你好|是|
|id|int|问题唯一id|1|是|


```
/result
```
### Get参数

样例
```JSON
{
  "main-question1-acc": 0.88,
  "main-question2-acc": 0.99,
}
```

字段说明

|字段|类型|说明|样例|是否必需|
|:---:|:---:|:---:|:---:|:---:|
|main-question1-acc|float|模型1预测的准确率|0.88|是|
|main-question2-acc|float|模型1预测的准确率|0.99|是|

