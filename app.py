#!/usr/bin/env python
"""
유관순정신계승사업회 웹사이트 통합 실행 스크립트

실행 방법:
    python app.py              # 기본 실행 (포트 8000)
    python app.py --port 80    # 포트 지정
    python app.py --host 0.0.0.0  # 외부 접속 허용

접속 URL:
    - 웹사이트: http://localhost:8000/
    - 관리자: http://localhost:8000/admin/
    - API: http://localhost:8000/api/v1/
"""
import os
import sys
import argparse
import subprocess

def main():
    # 인자 파싱
    parser = argparse.ArgumentParser(description='Yu Gwan-sun Memorial Association Web Server')
    parser.add_argument('--host', default='127.0.0.1', help='Host address (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8000, help='Port number (default: 8000)')
    args = parser.parse_args()

    # 프로젝트 경로 설정
    project_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(project_dir, 'backend')

    print(f"""
================================================================
    Yu Gwan-sun Memorial Association Web Server
================================================================
    Website:  http://{args.host}:{args.port}/
    Admin:    http://{args.host}:{args.port}/admin/
    API:      http://{args.host}:{args.port}/api/v1/
----------------------------------------------------------------
    Press Ctrl+C to stop the server
================================================================
""")

    # Django 서버 실행 (backend 폴더에서)
    try:
        subprocess.run(
            [sys.executable, 'manage.py', 'runserver', f'{args.host}:{args.port}'],
            cwd=backend_dir,
            check=True
        )
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except subprocess.CalledProcessError as e:
        print(f"Server error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
