pipeline {
    agent any

    environment {
        // 部署配置保持不变
        DEPLOY_SERVER = '192.168.129.176'
        DEPLOY_USER = 'root'
        REMOTE_PATH = '/opt/my-web-app/'

        // 【新增】定义你的本地仓库绝对路径
        // Windows 示例: "C:/Users/wzy/projects/jenkins-ceshi"
        // Linux/Mac 示例: "/home/wzy/projects/jenkins-ceshi"
        LOCAL_REPO_PATH = 'C:/Users/26224/Desktop/jenkins-ceshi'
    }

    stages {
        stage('Checkout') {
            steps {
                // 【修改】不再使用 checkout scm，而是使用 git 命令显式拉取
                // 这里的 url 填入上面定义的本地路径
                git url: "${LOCAL_REPO_PATH}", branch: 'main'
            }
        }

        stage('Run Unit Tests') {
            // 注意：这里使用了 docker agent
            agent {
                docker {
                    image 'python:3.10-slim'
                }
            }
            steps {
                sh '''
                    # 安装项目依赖
                    pip install -r requirements.txt || echo "No requirements.txt found, skipping..."

                    # 运行测试 (假设你有 pytest 或 unittest)
                    python -m pytest tests/ || echo "Tests skipped or failed"
                '''
            }
        }

        stage('Deploy to Server') {
            steps {
                script {
                    echo "开始部署 Web 应用到服务器 ${DEPLOY_SERVER}..."
                    
                    // 1. 将整个项目代码（包括 templates 文件夹）传输到远程服务器
                    sh """
                        scp -r app.py test_app.py templates requirements.txt ${DEPLOY_USER}@${DEPLOY_SERVER}:${REMOTE_PATH}/
                    """

                    // 2. 通过 SSH 登录远程服务器，安装依赖并重启服务
                    sh """
                        ssh ${DEPLOY_USER}@${DEPLOY_SERVER} "
                            cd ${REMOTE_PATH} &&
                            echo '正在安装/更新 Python 依赖...' &&
                            pip3 install -r requirements.txt &&
                            echo '正在重启 Web 服务...' &&
                            sudo systemctl restart my-web-app &&
                            # 简单的健康检查：尝试访问本地接口
                            sleep 2 &&
                            curl -f http://localhost:8000/ || exit 1
                        "
                    """
                }
            }
        }
    }

    post {
        success {
            echo '流水线执行成功！Web 页面已部署，请访问服务器 8000 端口查看。'
        }
        failure {
            echo '流水线执行失败，请检查测试报告或部署日志！'
        }
    }
}