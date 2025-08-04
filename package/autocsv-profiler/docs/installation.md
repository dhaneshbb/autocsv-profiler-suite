# Installation Guide

This guide covers the installation process for AutoCSV Profiler across different platforms and environments.

## System Requirements

### Minimum Requirements
- Python 3.9 or higher
- 2GB RAM (4GB recommended for large datasets)
- 500MB free disk space
- Internet connection for package downloads

### Supported Platforms
- Windows 10/11
- macOS 10.14 or later
- Linux (Ubuntu 18.04+, CentOS 7+, or equivalent)

### Python Version Support

<img src="data:image/svg+xml;base64,PHN2ZyBhcmlhLXJvbGVkZXNjcmlwdGlvbj0iZmxvd2NoYXJ0LXYyIiByb2xlPSJncmFwaGljcy1kb2N1bWVudCBkb2N1bWVudCIgdmlld0JveD0iMCAwIDQ1NS4zNTkzNzUgMzgyIiBzdHlsZT0ibWF4LXdpZHRoOiA0NTUuMzU5cHg7IGJhY2tncm91bmQtY29sb3I6IHdoaXRlOyIgY2xhc3M9ImZsb3djaGFydCIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgd2lkdGg9IjEwMCUiIGlkPSJteS1zdmciPjxzdHlsZT4jbXktc3Zne2ZvbnQtZmFtaWx5OiJ0cmVidWNoZXQgbXMiLHZlcmRhbmEsYXJpYWwsc2Fucy1zZXJpZjtmb250LXNpemU6MTZweDtmaWxsOiMzMzM7fUBrZXlmcmFtZXMgZWRnZS1hbmltYXRpb24tZnJhbWV7ZnJvbXtzdHJva2UtZGFzaG9mZnNldDowO319QGtleWZyYW1lcyBkYXNoe3Rve3N0cm9rZS1kYXNob2Zmc2V0OjA7fX0jbXktc3ZnIC5lZGdlLWFuaW1hdGlvbi1zbG93e3N0cm9rZS1kYXNoYXJyYXk6OSw1IWltcG9ydGFudDtzdHJva2UtZGFzaG9mZnNldDo5MDA7YW5pbWF0aW9uOmRhc2ggNTBzIGxpbmVhciBpbmZpbml0ZTtzdHJva2UtbGluZWNhcDpyb3VuZDt9I215LXN2ZyAuZWRnZS1hbmltYXRpb24tZmFzdHtzdHJva2UtZGFzaGFycmF5OjksNSFpbXBvcnRhbnQ7c3Ryb2tlLWRhc2hvZmZzZXQ6OTAwO2FuaW1hdGlvbjpkYXNoIDIwcyBsaW5lYXIgaW5maW5pdGU7c3Ryb2tlLWxpbmVjYXA6cm91bmQ7fSNteS1zdmcgLmVycm9yLWljb257ZmlsbDojNTUyMjIyO30jbXktc3ZnIC5lcnJvci10ZXh0e2ZpbGw6IzU1MjIyMjtzdHJva2U6IzU1MjIyMjt9I215LXN2ZyAuZWRnZS10aGlja25lc3Mtbm9ybWFse3N0cm9rZS13aWR0aDoxcHg7fSNteS1zdmcgLmVkZ2UtdGhpY2tuZXNzLXRoaWNre3N0cm9rZS13aWR0aDozLjVweDt9I215LXN2ZyAuZWRnZS1wYXR0ZXJuLXNvbGlke3N0cm9rZS1kYXNoYXJyYXk6MDt9I215LXN2ZyAuZWRnZS10aGlja25lc3MtaW52aXNpYmxle3N0cm9rZS13aWR0aDowO2ZpbGw6bm9uZTt9I215LXN2ZyAuZWRnZS1wYXR0ZXJuLWRhc2hlZHtzdHJva2UtZGFzaGFycmF5OjM7fSNteS1zdmcgLmVkZ2UtcGF0dGVybi1kb3R0ZWR7c3Ryb2tlLWRhc2hhcnJheToyO30jbXktc3ZnIC5tYXJrZXJ7ZmlsbDojMzMzMzMzO3N0cm9rZTojMzMzMzMzO30jbXktc3ZnIC5tYXJrZXIuY3Jvc3N7c3Ryb2tlOiMzMzMzMzM7fSNteS1zdmcgc3Zne2ZvbnQtZmFtaWx5OiJ0cmVidWNoZXQgbXMiLHZlcmRhbmEsYXJpYWwsc2Fucy1zZXJpZjtmb250LXNpemU6MTZweDt9I215LXN2ZyBwe21hcmdpbjowO30jbXktc3ZnIC5sYWJlbHtmb250LWZhbWlseToidHJlYnVjaGV0IG1zIix2ZXJkYW5hLGFyaWFsLHNhbnMtc2VyaWY7Y29sb3I6IzMzMzt9I215LXN2ZyAuY2x1c3Rlci1sYWJlbCB0ZXh0e2ZpbGw6IzMzMzt9I215LXN2ZyAuY2x1c3Rlci1sYWJlbCBzcGFue2NvbG9yOiMzMzM7fSNteS1zdmcgLmNsdXN0ZXItbGFiZWwgc3BhbiBwe2JhY2tncm91bmQtY29sb3I6dHJhbnNwYXJlbnQ7fSNteS1zdmcgLmxhYmVsIHRleHQsI215LXN2ZyBzcGFue2ZpbGw6IzMzMztjb2xvcjojMzMzO30jbXktc3ZnIC5ub2RlIHJlY3QsI215LXN2ZyAubm9kZSBjaXJjbGUsI215LXN2ZyAubm9kZSBlbGxpcHNlLCNteS1zdmcgLm5vZGUgcG9seWdvbiwjbXktc3ZnIC5ub2RlIHBhdGh7ZmlsbDojRUNFQ0ZGO3N0cm9rZTojOTM3MERCO3N0cm9rZS13aWR0aDoxcHg7fSNteS1zdmcgLnJvdWdoLW5vZGUgLmxhYmVsIHRleHQsI215LXN2ZyAubm9kZSAubGFiZWwgdGV4dCwjbXktc3ZnIC5pbWFnZS1zaGFwZSAubGFiZWwsI215LXN2ZyAuaWNvbi1zaGFwZSAubGFiZWx7dGV4dC1hbmNob3I6bWlkZGxlO30jbXktc3ZnIC5ub2RlIC5rYXRleCBwYXRoe2ZpbGw6IzAwMDtzdHJva2U6IzAwMDtzdHJva2Utd2lkdGg6MXB4O30jbXktc3ZnIC5yb3VnaC1ub2RlIC5sYWJlbCwjbXktc3ZnIC5ub2RlIC5sYWJlbCwjbXktc3ZnIC5pbWFnZS1zaGFwZSAubGFiZWwsI215LXN2ZyAuaWNvbi1zaGFwZSAubGFiZWx7dGV4dC1hbGlnbjpjZW50ZXI7fSNteS1zdmcgLm5vZGUuY2xpY2thYmxle2N1cnNvcjpwb2ludGVyO30jbXktc3ZnIC5yb290IC5hbmNob3IgcGF0aHtmaWxsOiMzMzMzMzMhaW1wb3J0YW50O3N0cm9rZS13aWR0aDowO3N0cm9rZTojMzMzMzMzO30jbXktc3ZnIC5hcnJvd2hlYWRQYXRoe2ZpbGw6IzMzMzMzMzt9I215LXN2ZyAuZWRnZVBhdGggLnBhdGh7c3Ryb2tlOiMzMzMzMzM7c3Ryb2tlLXdpZHRoOjIuMHB4O30jbXktc3ZnIC5mbG93Y2hhcnQtbGlua3tzdHJva2U6IzMzMzMzMztmaWxsOm5vbmU7fSNteS1zdmcgLmVkZ2VMYWJlbHtiYWNrZ3JvdW5kLWNvbG9yOnJnYmEoMjMyLDIzMiwyMzIsIDAuOCk7dGV4dC1hbGlnbjpjZW50ZXI7fSNteS1zdmcgLmVkZ2VMYWJlbCBwe2JhY2tncm91bmQtY29sb3I6cmdiYSgyMzIsMjMyLDIzMiwgMC44KTt9I215LXN2ZyAuZWRnZUxhYmVsIHJlY3R7b3BhY2l0eTowLjU7YmFja2dyb3VuZC1jb2xvcjpyZ2JhKDIzMiwyMzIsMjMyLCAwLjgpO2ZpbGw6cmdiYSgyMzIsMjMyLDIzMiwgMC44KTt9I215LXN2ZyAubGFiZWxCa2d7YmFja2dyb3VuZC1jb2xvcjpyZ2JhKDIzMiwgMjMyLCAyMzIsIDAuNSk7fSNteS1zdmcgLmNsdXN0ZXIgcmVjdHtmaWxsOiNmZmZmZGU7c3Ryb2tlOiNhYWFhMzM7c3Ryb2tlLXdpZHRoOjFweDt9I215LXN2ZyAuY2x1c3RlciB0ZXh0e2ZpbGw6IzMzMzt9I215LXN2ZyAuY2x1c3RlciBzcGFue2NvbG9yOiMzMzM7fSNteS1zdmcgZGl2Lm1lcm1haWRUb29sdGlwe3Bvc2l0aW9uOmFic29sdXRlO3RleHQtYWxpZ246Y2VudGVyO21heC13aWR0aDoyMDBweDtwYWRkaW5nOjJweDtmb250LWZhbWlseToidHJlYnVjaGV0IG1zIix2ZXJkYW5hLGFyaWFsLHNhbnMtc2VyaWY7Zm9udC1zaXplOjEycHg7YmFja2dyb3VuZDpoc2woODAsIDEwMCUsIDk2LjI3NDUwOTgwMzklKTtib3JkZXI6MXB4IHNvbGlkICNhYWFhMzM7Ym9yZGVyLXJhZGl1czoycHg7cG9pbnRlci1ldmVudHM6bm9uZTt6LWluZGV4OjEwMDt9I215LXN2ZyAuZmxvd2NoYXJ0VGl0bGVUZXh0e3RleHQtYW5jaG9yOm1pZGRsZTtmb250LXNpemU6MThweDtmaWxsOiMzMzM7fSNteS1zdmcgcmVjdC50ZXh0e2ZpbGw6bm9uZTtzdHJva2Utd2lkdGg6MDt9I215LXN2ZyAuaWNvbi1zaGFwZSwjbXktc3ZnIC5pbWFnZS1zaGFwZXtiYWNrZ3JvdW5kLWNvbG9yOnJnYmEoMjMyLDIzMiwyMzIsIDAuOCk7dGV4dC1hbGlnbjpjZW50ZXI7fSNteS1zdmcgLmljb24tc2hhcGUgcCwjbXktc3ZnIC5pbWFnZS1zaGFwZSBwe2JhY2tncm91bmQtY29sb3I6cmdiYSgyMzIsMjMyLDIzMiwgMC44KTtwYWRkaW5nOjJweDt9I215LXN2ZyAuaWNvbi1zaGFwZSByZWN0LCNteS1zdmcgLmltYWdlLXNoYXBlIHJlY3R7b3BhY2l0eTowLjU7YmFja2dyb3VuZC1jb2xvcjpyZ2JhKDIzMiwyMzIsMjMyLCAwLjgpO2ZpbGw6cmdiYSgyMzIsMjMyLDIzMiwgMC44KTt9I215LXN2ZyAubGFiZWwtaWNvbntkaXNwbGF5OmlubGluZS1ibG9jaztoZWlnaHQ6MWVtO292ZXJmbG93OnZpc2libGU7dmVydGljYWwtYWxpZ246LTAuMTI1ZW07fSNteS1zdmcgLm5vZGUgLmxhYmVsLWljb24gcGF0aHtmaWxsOmN1cnJlbnRDb2xvcjtzdHJva2U6cmV2ZXJ0O3N0cm9rZS13aWR0aDpyZXZlcnQ7fSNteS1zdmcgOnJvb3R7LS1tZXJtYWlkLWZvbnQtZmFtaWx5OiJ0cmVidWNoZXQgbXMiLHZlcmRhbmEsYXJpYWwsc2Fucy1zZXJpZjt9PC9zdHlsZT48Zz48bWFya2VyIG9yaWVudD0iYXV0byIgbWFya2VySGVpZ2h0PSI4IiBtYXJrZXJXaWR0aD0iOCIgbWFya2VyVW5pdHM9InVzZXJTcGFjZU9uVXNlIiByZWZZPSI1IiByZWZYPSI1IiB2aWV3Qm94PSIwIDAgMTAgMTAiIGNsYXNzPSJtYXJrZXIgZmxvd2NoYXJ0LXYyIiBpZD0ibXktc3ZnX2Zsb3djaGFydC12Mi1wb2ludEVuZCI+PHBhdGggc3R5bGU9InN0cm9rZS13aWR0aDogMTsgc3Ryb2tlLWRhc2hhcnJheTogMSwgMDsiIGNsYXNzPSJhcnJvd01hcmtlclBhdGgiIGQ9Ik0gMCAwIEwgMTAgNSBMIDAgMTAgeiIvPjwvbWFya2VyPjxtYXJrZXIgb3JpZW50PSJhdXRvIiBtYXJrZXJIZWlnaHQ9IjgiIG1hcmtlcldpZHRoPSI4IiBtYXJrZXJVbml0cz0idXNlclNwYWNlT25Vc2UiIHJlZlk9IjUiIHJlZlg9IjQuNSIgdmlld0JveD0iMCAwIDEwIDEwIiBjbGFzcz0ibWFya2VyIGZsb3djaGFydC12MiIgaWQ9Im15LXN2Z19mbG93Y2hhcnQtdjItcG9pbnRTdGFydCI+PHBhdGggc3R5bGU9InN0cm9rZS13aWR0aDogMTsgc3Ryb2tlLWRhc2hhcnJheTogMSwgMDsiIGNsYXNzPSJhcnJvd01hcmtlclBhdGgiIGQ9Ik0gMCA1IEwgMTAgMTAgTCAxMCAwIHoiLz48L21hcmtlcj48bWFya2VyIG9yaWVudD0iYXV0byIgbWFya2VySGVpZ2h0PSIxMSIgbWFya2VyV2lkdGg9IjExIiBtYXJrZXJVbml0cz0idXNlclNwYWNlT25Vc2UiIHJlZlk9IjUiIHJlZlg9IjExIiB2aWV3Qm94PSIwIDAgMTAgMTAiIGNsYXNzPSJtYXJrZXIgZmxvd2NoYXJ0LXYyIiBpZD0ibXktc3ZnX2Zsb3djaGFydC12Mi1jaXJjbGVFbmQiPjxjaXJjbGUgc3R5bGU9InN0cm9rZS13aWR0aDogMTsgc3Ryb2tlLWRhc2hhcnJheTogMSwgMDsiIGNsYXNzPSJhcnJvd01hcmtlclBhdGgiIHI9IjUiIGN5PSI1IiBjeD0iNSIvPjwvbWFya2VyPjxtYXJrZXIgb3JpZW50PSJhdXRvIiBtYXJrZXJIZWlnaHQ9IjExIiBtYXJrZXJXaWR0aD0iMTEiIG1hcmtlclVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgcmVmWT0iNSIgcmVmWD0iLTEiIHZpZXdCb3g9IjAgMCAxMCAxMCIgY2xhc3M9Im1hcmtlciBmbG93Y2hhcnQtdjIiIGlkPSJteS1zdmdfZmxvd2NoYXJ0LXYyLWNpcmNsZVN0YXJ0Ij48Y2lyY2xlIHN0eWxlPSJzdHJva2Utd2lkdGg6IDE7IHN0cm9rZS1kYXNoYXJyYXk6IDEsIDA7IiBjbGFzcz0iYXJyb3dNYXJrZXJQYXRoIiByPSI1IiBjeT0iNSIgY3g9IjUiLz48L21hcmtlcj48bWFya2VyIG9yaWVudD0iYXV0byIgbWFya2VySGVpZ2h0PSIxMSIgbWFya2VyV2lkdGg9IjExIiBtYXJrZXJVbml0cz0idXNlclNwYWNlT25Vc2UiIHJlZlk9IjUuMiIgcmVmWD0iMTIiIHZpZXdCb3g9IjAgMCAxMSAxMSIgY2xhc3M9Im1hcmtlciBjcm9zcyBmbG93Y2hhcnQtdjIiIGlkPSJteS1zdmdfZmxvd2NoYXJ0LXYyLWNyb3NzRW5kIj48cGF0aCBzdHlsZT0ic3Ryb2tlLXdpZHRoOiAyOyBzdHJva2UtZGFzaGFycmF5OiAxLCAwOyIgY2xhc3M9ImFycm93TWFya2VyUGF0aCIgZD0iTSAxLDEgbCA5LDkgTSAxMCwxIGwgLTksOSIvPjwvbWFya2VyPjxtYXJrZXIgb3JpZW50PSJhdXRvIiBtYXJrZXJIZWlnaHQ9IjExIiBtYXJrZXJXaWR0aD0iMTEiIG1hcmtlclVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgcmVmWT0iNS4yIiByZWZYPSItMSIgdmlld0JveD0iMCAwIDExIDExIiBjbGFzcz0ibWFya2VyIGNyb3NzIGZsb3djaGFydC12MiIgaWQ9Im15LXN2Z19mbG93Y2hhcnQtdjItY3Jvc3NTdGFydCI+PHBhdGggc3R5bGU9InN0cm9rZS13aWR0aDogMjsgc3Ryb2tlLWRhc2hhcnJheTogMSwgMDsiIGNsYXNzPSJhcnJvd01hcmtlclBhdGgiIGQ9Ik0gMSwxIGwgOSw5IE0gMTAsMSBsIC05LDkiLz48L21hcmtlcj48ZyBjbGFzcz0icm9vdCI+PGcgY2xhc3M9ImNsdXN0ZXJzIi8+PGcgY2xhc3M9ImVkZ2VQYXRocyI+PHBhdGggbWFya2VyLWVuZD0idXJsKCNteS1zdmdfZmxvd2NoYXJ0LXYyLXBvaW50RW5kKSIgc3R5bGU9IiIgY2xhc3M9ImVkZ2UtdGhpY2tuZXNzLW5vcm1hbCBlZGdlLXBhdHRlcm4tc29saWQgZWRnZS10aGlja25lc3Mtbm9ybWFsIGVkZ2UtcGF0dGVybi1zb2xpZCBmbG93Y2hhcnQtbGluayIgaWQ9IkxfQV9CXzAiIGQ9Ik0xMTMuMzMxLDE2NEwxMjguNjQzLDE0Mi41QzE0My45NTUsMTIxLDE3NC41NzksNzgsMjAzLjE5OCw1Ni41QzIzMS44MTgsMzUsMjU4LjQzMiwzNSwyNzEuNzQsMzVMMjg1LjA0NywzNSIvPjxwYXRoIG1hcmtlci1lbmQ9InVybCgjbXktc3ZnX2Zsb3djaGFydC12Mi1wb2ludEVuZCkiIHN0eWxlPSIiIGNsYXNzPSJlZGdlLXRoaWNrbmVzcy1ub3JtYWwgZWRnZS1wYXR0ZXJuLXNvbGlkIGVkZ2UtdGhpY2tuZXNzLW5vcm1hbCBlZGdlLXBhdHRlcm4tc29saWQgZmxvd2NoYXJ0LWxpbmsiIGlkPSJMX0FfQ18wIiBkPSJNMTUxLjc4OSwxNjRMMTYwLjY5MSwxNTkuODMzQzE2OS41OTQsMTU1LjY2NywxODcuMzk4LDE0Ny4zMzMsMjA4LjkwOSwxNDMuMTY3QzIzMC40MTksMTM5LDI1NS42MzUsMTM5LDI2OC4yNDMsMTM5TDI4MC44NTIsMTM5Ii8+PHBhdGggbWFya2VyLWVuZD0idXJsKCNteS1zdmdfZmxvd2NoYXJ0LXYyLXBvaW50RW5kKSIgc3R5bGU9IiIgY2xhc3M9ImVkZ2UtdGhpY2tuZXNzLW5vcm1hbCBlZGdlLXBhdHRlcm4tc29saWQgZWRnZS10aGlja25lc3Mtbm9ybWFsIGVkZ2UtcGF0dGVybi1zb2xpZCBmbG93Y2hhcnQtbGluayIgaWQ9IkxfQV9EXzAiIGQ9Ik0xNTEuNzg5LDIxOEwxNjAuNjkxLDIyMi4xNjdDMTY5LjU5NCwyMjYuMzMzLDE4Ny4zOTgsMjM0LjY2NywxOTkuODAxLDIzOC44MzNDMjEyLjIwMywyNDMsMjE5LjIwMywyNDMsMjIyLjcwMywyNDNMMjI2LjIwMywyNDMiLz48cGF0aCBtYXJrZXItZW5kPSJ1cmwoI215LXN2Z19mbG93Y2hhcnQtdjItcG9pbnRFbmQpIiBzdHlsZT0iIiBjbGFzcz0iZWRnZS10aGlja25lc3Mtbm9ybWFsIGVkZ2UtcGF0dGVybi1zb2xpZCBlZGdlLXRoaWNrbmVzcy1ub3JtYWwgZWRnZS1wYXR0ZXJuLXNvbGlkIGZsb3djaGFydC1saW5rIiBpZD0iTF9BX0VfMCIgZD0iTTExMy4zMzEsMjE4TDEyOC42NDMsMjM5LjVDMTQzLjk1NSwyNjEsMTc0LjU3OSwzMDQsMjAyLjQ5OSwzMjUuNUMyMzAuNDE5LDM0NywyNTUuNjM1LDM0NywyNjguMjQzLDM0N0wyODAuODUyLDM0NyIvPjwvZz48ZyBjbGFzcz0iZWRnZUxhYmVscyI+PGcgY2xhc3M9ImVkZ2VMYWJlbCI+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMCwgMCkiIGNsYXNzPSJsYWJlbCI+PGZvcmVpZ25PYmplY3QgaGVpZ2h0PSIwIiB3aWR0aD0iMCI+PGRpdiBzdHlsZT0iZGlzcGxheTogdGFibGUtY2VsbDsgd2hpdGUtc3BhY2U6IG5vd3JhcDsgbGluZS1oZWlnaHQ6IDEuNTsgbWF4LXdpZHRoOiAyMDBweDsgdGV4dC1hbGlnbjogY2VudGVyOyIgY2xhc3M9ImxhYmVsQmtnIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94aHRtbCI+PHNwYW4gY2xhc3M9ImVkZ2VMYWJlbCI+PC9zcGFuPjwvZGl2PjwvZm9yZWlnbk9iamVjdD48L2c+PC9nPjxnIGNsYXNzPSJlZGdlTGFiZWwiPjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAsIDApIiBjbGFzcz0ibGFiZWwiPjxmb3JlaWduT2JqZWN0IGhlaWdodD0iMCIgd2lkdGg9IjAiPjxkaXYgc3R5bGU9ImRpc3BsYXk6IHRhYmxlLWNlbGw7IHdoaXRlLXNwYWNlOiBub3dyYXA7IGxpbmUtaGVpZ2h0OiAxLjU7IG1heC13aWR0aDogMjAwcHg7IHRleHQtYWxpZ246IGNlbnRlcjsiIGNsYXNzPSJsYWJlbEJrZyIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGh0bWwiPjxzcGFuIGNsYXNzPSJlZGdlTGFiZWwiPjwvc3Bhbj48L2Rpdj48L2ZvcmVpZ25PYmplY3Q+PC9nPjwvZz48ZyBjbGFzcz0iZWRnZUxhYmVsIj48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgwLCAwKSIgY2xhc3M9ImxhYmVsIj48Zm9yZWlnbk9iamVjdCBoZWlnaHQ9IjAiIHdpZHRoPSIwIj48ZGl2IHN0eWxlPSJkaXNwbGF5OiB0YWJsZS1jZWxsOyB3aGl0ZS1zcGFjZTogbm93cmFwOyBsaW5lLWhlaWdodDogMS41OyBtYXgtd2lkdGg6IDIwMHB4OyB0ZXh0LWFsaWduOiBjZW50ZXI7IiBjbGFzcz0ibGFiZWxCa2ciIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIj48c3BhbiBjbGFzcz0iZWRnZUxhYmVsIj48L3NwYW4+PC9kaXY+PC9mb3JlaWduT2JqZWN0PjwvZz48L2c+PGcgY2xhc3M9ImVkZ2VMYWJlbCI+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMCwgMCkiIGNsYXNzPSJsYWJlbCI+PGZvcmVpZ25PYmplY3QgaGVpZ2h0PSIwIiB3aWR0aD0iMCI+PGRpdiBzdHlsZT0iZGlzcGxheTogdGFibGUtY2VsbDsgd2hpdGUtc3BhY2U6IG5vd3JhcDsgbGluZS1oZWlnaHQ6IDEuNTsgbWF4LXdpZHRoOiAyMDBweDsgdGV4dC1hbGlnbjogY2VudGVyOyIgY2xhc3M9ImxhYmVsQmtnIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94aHRtbCI+PHNwYW4gY2xhc3M9ImVkZ2VMYWJlbCI+PC9zcGFuPjwvZGl2PjwvZm9yZWlnbk9iamVjdD48L2c+PC9nPjwvZz48ZyBjbGFzcz0ibm9kZXMiPjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDk0LjEwMTU2MjUsIDE5MSkiIGlkPSJmbG93Y2hhcnQtQS0wIiBjbGFzcz0ibm9kZSBkZWZhdWx0Ij48cmVjdCBoZWlnaHQ9IjU0IiB3aWR0aD0iMTcyLjIwMzEyNSIgeT0iLTI3IiB4PSItODYuMTAxNTYyNSIgc3R5bGU9IiIgY2xhc3M9ImJhc2ljIGxhYmVsLWNvbnRhaW5lciIvPjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKC01Ni4xMDE1NjI1LCAtMTIpIiBzdHlsZT0iIiBjbGFzcz0ibGFiZWwiPjxyZWN0Lz48Zm9yZWlnbk9iamVjdCBoZWlnaHQ9IjI0IiB3aWR0aD0iMTEyLjIwMzEyNSI+PGRpdiBzdHlsZT0iZGlzcGxheTogdGFibGUtY2VsbDsgd2hpdGUtc3BhY2U6IG5vd3JhcDsgbGluZS1oZWlnaHQ6IDEuNTsgbWF4LXdpZHRoOiAyMDBweDsgdGV4dC1hbGlnbjogY2VudGVyOyIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGh0bWwiPjxzcGFuIGNsYXNzPSJub2RlTGFiZWwiPjxwPlB5dGhvbiBWZXJzaW9uczwvcD48L3NwYW4+PC9kaXY+PC9mb3JlaWduT2JqZWN0PjwvZz48L2c+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMzM4Ljc4MTI1LCAzNSkiIGlkPSJmbG93Y2hhcnQtQi0xIiBjbGFzcz0ibm9kZSBkZWZhdWx0Ij48cmVjdCBoZWlnaHQ9IjU0IiB3aWR0aD0iOTkuNDY4NzUiIHk9Ii0yNyIgeD0iLTQ5LjczNDM3NSIgc3R5bGU9IiIgY2xhc3M9ImJhc2ljIGxhYmVsLWNvbnRhaW5lciIvPjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xOS43MzQzNzUsIC0xMikiIHN0eWxlPSIiIGNsYXNzPSJsYWJlbCI+PHJlY3QvPjxmb3JlaWduT2JqZWN0IGhlaWdodD0iMjQiIHdpZHRoPSIzOS40Njg3NSI+PGRpdiBzdHlsZT0iZGlzcGxheTogdGFibGUtY2VsbDsgd2hpdGUtc3BhY2U6IG5vd3JhcDsgbGluZS1oZWlnaHQ6IDEuNTsgbWF4LXdpZHRoOiAyMDBweDsgdGV4dC1hbGlnbjogY2VudGVyOyIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGh0bWwiPjxzcGFuIGNsYXNzPSJub2RlTGFiZWwiPjxwPjMuOSDinJM8L3A+PC9zcGFuPjwvZGl2PjwvZm9yZWlnbk9iamVjdD48L2c+PC9nPjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDMzOC43ODEyNSwgMTM5KSIgaWQ9ImZsb3djaGFydC1DLTMiIGNsYXNzPSJub2RlIGRlZmF1bHQiPjxyZWN0IGhlaWdodD0iNTQiIHdpZHRoPSIxMDcuODU5Mzc1IiB5PSItMjciIHg9Ii01My45Mjk2ODc1IiBzdHlsZT0iIiBjbGFzcz0iYmFzaWMgbGFiZWwtY29udGFpbmVyIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTIzLjkyOTY4NzUsIC0xMikiIHN0eWxlPSIiIGNsYXNzPSJsYWJlbCI+PHJlY3QvPjxmb3JlaWduT2JqZWN0IGhlaWdodD0iMjQiIHdpZHRoPSI0Ny44NTkzNzUiPjxkaXYgc3R5bGU9ImRpc3BsYXk6IHRhYmxlLWNlbGw7IHdoaXRlLXNwYWNlOiBub3dyYXA7IGxpbmUtaGVpZ2h0OiAxLjU7IG1heC13aWR0aDogMjAwcHg7IHRleHQtYWxpZ246IGNlbnRlcjsiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hodG1sIj48c3BhbiBjbGFzcz0ibm9kZUxhYmVsIj48cD4zLjEwIOKckzwvcD48L3NwYW4+PC9kaXY+PC9mb3JlaWduT2JqZWN0PjwvZz48L2c+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMzM4Ljc4MTI1LCAyNDMpIiBpZD0iZmxvd2NoYXJ0LUQtNSIgY2xhc3M9Im5vZGUgZGVmYXVsdCI+PHJlY3QgaGVpZ2h0PSI1NCIgd2lkdGg9IjIxNy4xNTYyNSIgeT0iLTI3IiB4PSItMTA4LjU3ODEyNSIgc3R5bGU9ImZpbGw6I2U4ZjVlOCAhaW1wb3J0YW50IiBjbGFzcz0iYmFzaWMgbGFiZWwtY29udGFpbmVyIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTc4LjU3ODEyNSwgLTEyKSIgc3R5bGU9IiIgY2xhc3M9ImxhYmVsIj48cmVjdC8+PGZvcmVpZ25PYmplY3QgaGVpZ2h0PSIyNCIgd2lkdGg9IjE1Ny4xNTYyNSI+PGRpdiBzdHlsZT0iZGlzcGxheTogdGFibGUtY2VsbDsgd2hpdGUtc3BhY2U6IG5vd3JhcDsgbGluZS1oZWlnaHQ6IDEuNTsgbWF4LXdpZHRoOiAyMDBweDsgdGV4dC1hbGlnbjogY2VudGVyOyIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGh0bWwiPjxzcGFuIGNsYXNzPSJub2RlTGFiZWwiPjxwPjMuMTEg4pyTIFJlY29tbWVuZGVkPC9wPjwvc3Bhbj48L2Rpdj48L2ZvcmVpZ25PYmplY3Q+PC9nPjwvZz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgzMzguNzgxMjUsIDM0NykiIGlkPSJmbG93Y2hhcnQtRS03IiBjbGFzcz0ibm9kZSBkZWZhdWx0Ij48cmVjdCBoZWlnaHQ9IjU0IiB3aWR0aD0iMTA3Ljg1OTM3NSIgeT0iLTI3IiB4PSItNTMuOTI5Njg3NSIgc3R5bGU9IiIgY2xhc3M9ImJhc2ljIGxhYmVsLWNvbnRhaW5lciIvPjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0yMy45Mjk2ODc1LCAtMTIpIiBzdHlsZT0iIiBjbGFzcz0ibGFiZWwiPjxyZWN0Lz48Zm9yZWlnbk9iamVjdCBoZWlnaHQ9IjI0IiB3aWR0aD0iNDcuODU5Mzc1Ij48ZGl2IHN0eWxlPSJkaXNwbGF5OiB0YWJsZS1jZWxsOyB3aGl0ZS1zcGFjZTogbm93cmFwOyBsaW5lLWhlaWdodDogMS41OyBtYXgtd2lkdGg6IDIwMHB4OyB0ZXh0LWFsaWduOiBjZW50ZXI7IiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94aHRtbCI+PHNwYW4gY2xhc3M9Im5vZGVMYWJlbCI+PHA+My4xMiDinJM8L3A+PC9zcGFuPjwvZGl2PjwvZm9yZWlnbk9iamVjdD48L2c+PC9nPjwvZz48L2c+PC9nPjwvc3ZnPg==" alt="Python Version Support" width="600">

## Installation Methods

### Method 1: PyPI Installation (Recommended)

#### Basic Installation
```bash
pip install autocsv-profiler
```

#### With Development Dependencies
```bash
pip install autocsv-profiler[dev]
```

#### Upgrade to Latest Version
```bash
pip install --upgrade autocsv-profiler
```

### Method 2: Conda Installation

#### Using conda-forge
```bash
conda install -c conda-forge autocsv-profiler
```

#### In New Environment
```bash
conda create -n csv-analysis python=3.11
conda activate csv-analysis
pip install autocsv-profiler
```

### Method 3: Source Installation

#### From GitHub
```bash
git clone https://github.com/dhaneshbb/AutoCSV-Profiler-Suite.git
cd AutoCSV-Profiler-Suite
pip install .
```

#### Development Installation
```bash
git clone https://github.com/dhaneshbb/AutoCSV-Profiler-Suite.git
cd AutoCSV-Profiler-Suite
pip install -e .[dev]
```

## Platform-Specific Instructions

### Windows

#### Using Command Prompt
```cmd
# Install Python from python.org if not already installed
python -m pip install --upgrade pip
python -m pip install autocsv-profiler
```

#### Using PowerShell
```powershell
# Ensure execution policy allows script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install package
pip install autocsv-profiler
```

#### Using Anaconda Prompt
```bash
# Open Anaconda Prompt
conda create -n csvanalysis python=3.11
conda activate csvanalysis
pip install autocsv-profiler
```

### macOS

#### Using Terminal
```bash
# Install using pip
pip3 install autocsv-profiler

# Or using Homebrew Python
brew install python
pip3 install autocsv-profiler
```

#### Using Conda
```bash
# If using Anaconda/Miniconda
conda install -c conda-forge autocsv-profiler
```

### Linux (Ubuntu/Debian)

#### System Installation
```bash
# Update package list
sudo apt update

# Install Python and pip if not present
sudo apt install python3 python3-pip

# Install AutoCSV Profiler
pip3 install autocsv-profiler
```

#### User Installation
```bash
# Install for current user only
pip3 install --user autocsv-profiler

# Add to PATH if needed
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Linux (CentOS/RHEL)

```bash
# Install Python and pip
sudo yum install python3 python3-pip

# Install package
pip3 install autocsv-profiler
```

## Virtual Environment Setup

### Using venv (Recommended)

```bash
# Create virtual environment
python -m venv csvprofiler-env

# Activate environment
# Windows:
csvprofiler-env\Scripts\activate
# macOS/Linux:
source csvprofiler-env/bin/activate

# Install package
pip install autocsv-profiler

# Deactivate when done
deactivate
```

### Using conda

```bash
# Create conda environment
conda create -n csvprofiler python=3.11

# Activate environment
conda activate csvprofiler

# Install package
pip install autocsv-profiler

# Deactivate when done
conda deactivate
```

## Verification

### Test Installation
```bash
# Check if package is installed
pip show autocsv-profiler

# Verify command-line tool
autocsv-profiler --version

# Test Python import
python -c "import autocsv_profiler; print(f'AutoCSV Profiler v{autocsv_profiler.__version__} installed successfully!')"
```

### Quick Functionality Test
```bash
# Create a test CSV file
echo "name,age,city
Alice,25,New York
Bob,30,London
Carol,28,Paris" > test.csv

# Run analysis
autocsv-profiler test.csv

# Check output
ls test_analysis/
```

## Dependency Information

### Core Dependencies
```
pandas>=1.5.0          # Data manipulation
numpy>=1.24.0           # Numerical computing
scipy>=1.10.0           # Scientific computing
matplotlib>=3.6.0       # Plotting
seaborn>=0.12.0         # Statistical visualization
scikit-learn>=1.2.0     # Machine learning tools
statsmodels>=0.13.0     # Statistical modeling
tqdm>=4.64.0            # Progress bars
```

### Analysis-Specific Dependencies
```
tableone>=0.7.12        # Statistical summaries
missingno>=0.5.2        # Missing data visualization
tabulate>=0.9.0         # Table formatting
```

### Optional Dependencies (Development)
```
pytest>=7.0.0           # Testing framework
black>=22.0.0           # Code formatting
flake8>=6.0.0           # Code linting
mypy>=0.991             # Type checking
```

## Installation Troubleshooting

### Common Issues

#### Permission Errors
```bash
# Use --user flag for user installation
pip install --user autocsv-profiler

# Or use virtual environment
python -m venv myenv
source myenv/bin/activate  # Linux/Mac
# or myenv\Scripts\activate  # Windows
pip install autocsv-profiler
```

#### Dependency Conflicts
```bash
# Create fresh environment
conda create -n fresh-env python=3.11
conda activate fresh-env
pip install autocsv-profiler
```

#### Network Issues
```bash
# Use different index
pip install -i https://pypi.org/simple/ autocsv-profiler

# Or upgrade pip first
python -m pip install --upgrade pip
pip install autocsv-profiler
```

#### Python Version Issues
```bash
# Check Python version
python --version

# Use specific Python version
python3.11 -m pip install autocsv-profiler
```

### Platform-Specific Issues

#### Windows Path Issues
```cmd
# Add Python Scripts to PATH
set PATH=%PATH%;%LOCALAPPDATA%\Programs\Python\Python311\Scripts

# Or use python -m
python -m autocsv_profiler.cli data.csv
```

#### macOS Permission Issues
```bash
# Use --user installation
pip3 install --user autocsv-profiler

# Or use sudo (not recommended)
sudo pip3 install autocsv-profiler
```

#### Linux Package Manager Conflicts
```bash
# Use pip instead of system package manager
python3 -m pip install --user autocsv-profiler

# Or use pipx for isolated installation
pipx install autocsv-profiler
```

## Environment Variables

### Optional Configuration
```bash
# Set default output directory
export AUTOCSV_OUTPUT_DIR="/path/to/default/output"

# Set memory limit for large files
export AUTOCSV_MEMORY_LIMIT="4GB"

# Enable debug logging
export AUTOCSV_DEBUG=1
```

## Performance Optimization

### For Large Datasets
```bash
# Install with additional dependencies for performance
pip install autocsv-profiler pandas[performance]

# Or use conda for optimized packages
conda install -c conda-forge autocsv-profiler pandas numpy
```

### Memory Management
```bash
# Monitor memory usage during installation
pip install autocsv-profiler --no-cache-dir
```

## Uninstallation

### Remove Package
```bash
# Uninstall package
pip uninstall autocsv-profiler

# Remove dependencies (if not used by other packages)
pip uninstall pandas numpy matplotlib seaborn scipy scikit-learn statsmodels tqdm tableone missingno tabulate
```

### Clean Environment
```bash
# Remove virtual environment
rm -rf csvprofiler-env  # Linux/Mac
rmdir /s csvprofiler-env  # Windows

# Or remove conda environment
conda env remove -n csvprofiler
```

## Next Steps

After successful installation:

1. **Read the [Usage Guide](usage.md)** for detailed usage instructions
2. **Check [Examples](examples.md)** for sample analyses
3. **Review [API Reference](api-reference.md)** for programmatic usage
4. **See [Troubleshooting](troubleshooting.md)** if you encounter issues

## Getting Help

If you encounter installation issues:

1. Check the [Troubleshooting Guide](troubleshooting.md)
2. Search [GitHub Issues](https://github.com/dhaneshbb/AutoCSV-Profiler-Suite/issues)
3. Create a new issue with:
   - Operating system and version
   - Python version
   - Installation method used
   - Complete error message
   - Output of `pip list` or `conda list`