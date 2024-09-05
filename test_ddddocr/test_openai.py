import os
from openai import OpenAI

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "你是一名图像处理工程师，需要计划滑块的横向移动范围。滑块图片是2张图像的base64值，你找出横向移动的像素值，只需要回答像素值即可?.如下json中的slidingImage与originalImage一个表示滑块，一个表示背景图" +"""{"slidingImage": "iVBORw0KGgoAAAANSUhEUgAAACwAAAAsCAYAAAAehFoBAAACb0lEQVR42u2Xy2sTURTG+5foThe+NsVqMzFp1GoRtT5r8VFSEVRELdlVcNOdm6pQsNRgG4WQIClBS9CkSScVmrSIj2AynWAbIsEmiriTuPnMDbgQk3vv5NbhgvPBEGbOmXN+c3LmzL1tbZYsWbL0z4QGkhp2z/ADKJ77sA3dxe6bo/JCEyjX7Ukot8bRTNIBd408+QtMSmgC0j0abgpErisjPrmA941FqMC2OwG5gO3BJL3C957JBdwZogObCgsO7YymGr5Y5HyXNwojEoY9EEyjffE9NhY1bKnoaC9r2FbOYVMpiw0rGWzOvMP2xdfoiKWbTgnFn0SnLwHbVAKKbw7KZLx+OLyzsD+MwTEehWPshRg0ubFnQkWPPy1UHSPVdU3MigEf8s6b1n/1WT6ligH3Pk6bCrw3mBIDPhpYMhd45o0Y8OHwW1OBXfFM69ODOB2Paub2cCoH53wWXWoO+2tHdyKLg3MaHzgxnlbzpgLT1BtfZgP3JXQpPqlc7UEM/bG8NGsAZosSw7mILhXwiedZOvBAWJMKuH/6Ax3YHTIGvB6LmUb3/j6/8JQBPDi9zJ2U+Dl/luCsrsFRLUOp/RqFJr7HFlZxMvnxj4cmhbvoz7GnxKUQXw8Tn44aoL1aaXnw16fSQhFn1dXWYhCHy+E8dzLnj6/UTShPjMF4QezTfG1mhRmA2I98/8a1vGTFucqRjxrgeqTAlaivXKECn9fXuOJcCejmAJ8pfKEC31j6zBXH/UgQeOhlkfl3EtuOU551aYkBryAwkSf2ibm12aq4GyaqV/dVCR6VHYNUVwjY6H6sGbBoDEuWLFn6z/QL/TdjNJqBVrkAAAAASUVORK5CYII=",
        "originalImage": "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"}""",
        }
    ],
    model=model_name,
    temperature=1.,
    max_tokens=4096,
    top_p=1.
)

print(response.choices[0].message.content)