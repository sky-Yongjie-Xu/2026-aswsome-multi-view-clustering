from pathlib import Path
import json,collections,urllib.parse,csv
ROOT=Path(__file__).resolve().parents[1]
REPO="sky-Yongjie-Xu/2026-aswsome-multi-view-clustering"
WEB="https://github.com/"+REPO
papers=json.loads((ROOT/"catalog/papers.json").read_text())
def esc(s):return s.replace("|","\\|").replace("\n"," ")
def link(path):return WEB+"/blob/main/"+urllib.parse.quote(path)
def table(items):
 out=["| 年份 | 方法 | 论文 | 会议 | 阅读 | 补充材料 |","|---|---|---|---|---|---|"]
 for p in sorted(items,key=lambda x:(-x["year"],x["method"].casefold(),x["title"].casefold())):
  venue=p["venue"]+(" · 预印本" if p["publication_status"]=="preprint" else " · 已录用公开稿" if p["publication_status"]=="accepted" else "")
  reading=f'[在线阅读]({p.get("html_url") or (link(p["path"]) if (ROOT/p["path"]).exists() else p["pdf_sources"][0])}) · [原文 PDF]({p["pdf_sources"][0]})'
  if p.get("source_page"):reading+=f' · [论文主页]({p["source_page"]})'
  supp=" · ".join(f'[材料{i+1}]({link(s["path"])})' for i,s in enumerate(p["supplements"])) or "—"
  out.append(f'| {p["year"]} | **{esc(p["method"])}** | {esc(p["title"])} | {venue} | {reading} | {supp} |')
 return out
categories=sorted({x["category"] for x in papers})
lines=["# Awesome Incomplete & Noisy Multi-view Clustering","","聚焦**不完备、观测噪声和跨视图错配/不对齐**的多视图聚类文献。按研究方向分类，各方向内按发表年份**从新到旧**排列。","",f'清单包含 **{len(papers)} 篇文献**，仓库已归档 **{sum((ROOT/p["path"]).exists() for p in papers)} 篇正文**和 **{sum((ROOT/y["path"]).exists() for x in papers for y in x["supplements"])} 份独立补充材料**，主要覆盖 2024—2026 年顶会，并保留两篇 2023 年基础论文。',"","**阅读方式：**“在线阅读”优先打开已验证的 HTML 全文，无 HTML 全文时打开 GitHub 的 PDF 网页预览；“原文 PDF”打开作者或出版方公开全文；“论文主页”提供正式出版/录用信息，不等同于 HTML 全文。正文内附录随原 PDF 一并保留。","","[完整索引 CSV](catalog/papers.csv) · [结构化清单 JSON](catalog/papers.json) · [待补齐论文](catalog/pending.json) · [版本与版权说明](NOTICE.md)","","## 方向导航",""]
for i,cat in enumerate(categories,1):
 items=[p for p in papers if p["category"]==cat]
 label=" / ".join(part.split("_",1)[-1] for part in cat.split("/"))
 lines.append(f'- [{label}](#topic-{i})（{len(items)} 篇）')
for i,cat in enumerate(categories,1):
 items=[p for p in papers if p["category"]==cat];label=" / ".join(part.split("_",1)[-1] for part in cat.split("/"))
 lines += ["",f'<a id="topic-{i}"></a>',"",f'## {label}',""]+table(items)
 directory=ROOT/"papers"/cat;directory.mkdir(parents=True,exist_ok=True)
 (directory/"README.md").write_text("\n".join(["# "+label,"","[返回总目录]("+WEB+")",""]+table(items))+"\n")
lines += ["","## 更新与收录规则","","- 单篇正文只归档一次，避免同一论文在不同方向重复保存。","- 文件名采用 `年份-方法简称-会议简称.pdf`；无法可靠核实简称时保留描述性题名。","- 正式发表论文、已录用公开稿和预印本分别标注；不同实验条件不能直接混作基线。","- 该清单不是对近三年全部相关论文的穷尽保证，尚未取得全文的条目单独列入待补齐清单。","- 元数据更新后运行 `python scripts/build_readme.py` 重新生成总目录与各方向索引。",""]
(ROOT/"README.md").write_text("\n".join(lines))

with open(ROOT/"catalog/papers.csv","w",encoding="utf-8-sig",newline="") as f:
 w=csv.writer(f);w.writerow(["年份","方法","会议","方向","题名","在线阅读","原文PDF","论文主页","归档文件","补充材料","版本备注"])
 for p in papers:w.writerow([p["year"],p["method"],p["venue"],p["category"],p["title"],p.get("html_url") or (link(p["path"]) if (ROOT/p["path"]).exists() else p["pdf_sources"][0]),p["pdf_sources"][0],p["source_page"],p["path"],"; ".join(s["path"] for s in p["supplements"]),p["version_note"]])
