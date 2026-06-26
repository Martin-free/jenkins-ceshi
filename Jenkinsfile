pipeline {
    agent any

    environment {
        DEPLOY_SERVER = '192.168.129.176'
        DEPLOY_USER = 'root'
        REMOTE_PATH = '/opt/my-web-app'
        // 不需要定义 LOCAL_REPO_PATH 了
    }

    stages {
        stage('Checkout') {
            steps {
                // 直接使用 checkout scm，它会复用 Jenkins 任务配置里设置的 GitHub 地址
                // 这步其实可以省略，因为 Declarative Pipeline 默认会在开始前自动 checkout
                // 但写上也无妨，确保代码是最新的
                checkout scm
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