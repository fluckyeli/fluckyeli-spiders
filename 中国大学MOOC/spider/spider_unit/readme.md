# 课件json解析

## 课程

> mocTermDto.chapters.lessons.units[*]

| contentType 值 | 可能的含义 | 下载请求URL                                                                           |
|---------------|-------|-----------------------------------------------------------------------------------|
| 1             | 视频    | https://www.icourse163.org/dwr/call/plaincall/CourseBean.getLessonUnitLearnVo.dwr |
| 4             | 富文本   | 同上                                                                                |
| 6             | 讨论    | 同上                                                                                |
| 3             | 文档    | 同上                                                                                |
| 5             | 测验    | 同上                                                                                |
|               |       |                                                                                   |
|               |       |                                                                                   |
|               |       |                                                                                   |
|               |       |                                                                                   |

## homework

> mocTermDto.chapters.homeworks[*]
> | contentType 值 | 可能的含义 | 下载请求URL |
> |---------------|-------|-----------------------------------------------------------------------------------|
> | 3 | 文档 | https://www.icourse163.org/dwr/call/plaincall/YocOJQuizBean.getOJPaperDto.dwr  |
> | | | |
> | | | |
> | | | |

## 考试

> mocTermDto.exams[*]

https://www.icourse163.org/web/j/mocQuizRpcBean.getOpenQuizPaperDto.rpc?csrfKey=abb608c49f0e42f8a91bc33e2dbead4f