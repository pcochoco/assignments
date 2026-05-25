## 프로젝트 개요

AWS 환경에서 외부 접근 가능한 웹 서비스 인프라를 직접 설계하고 구축했습니다.  
네트워크 흐름과 보안 경계를 이해하는 데 중점을 두었으며, VPC 기반 네트워크 분리, 접근 제어, 최소 권한 정책을 적용해 구성했습니다.

## 주요 구현 내용

- VPC 및 Public Subnet 설계
- Internet Gateway 및 Route Table 구성
- EC2 인스턴스 배포 및 Nginx 기반 웹 서버 운영
- Security Group 기반 최소 포트 허용 정책 적용
- IAM 사용자 기반 최소 권한 접근 제어
- Public IP 기반 외부 접근 환경 구성
- 루트 계정 대신 IAM 사용자 기반 접근 적용

## 인프라 구조

<img width="747" height="443" alt="image" src="https://github.com/user-attachments/assets/02797c60-09df-4964-baae-10cb9022adbd" />


### IAM (Identity and Access Management)
사용자, 그룹, 권한 정책을 기반으로 AWS 리소스 접근을 제어하는 서비스
루트 계정 대신 IAM 사용자를 생성하고 최소 권한 정책을 적용했다.

### Internet Gateway
VPC와 외부 인터넷 간 통신을 위한 게이트웨이
Public Subnet의 Route Table과 연결하여 외부 요청 및 응답이 가능하도록 구성했다.

### EC2
AWS에서 제공하는 가상 서버 서비스
Ubuntu 환경에 Nginx를 설치하여 웹 서버를 구성하고 외부 접근 환경을 구축했다.

### Security Group
EC2와 같은 리소스 단위의 가상 방화벽
포트 및 IP 기반으로 Inbound / Outbound 트래픽을 제어하며 필요한 포트만 허용하도록 설정했다.

- SSH (22) : 개인 IP만 허용
- HTTP (80) : 외부 접근 허용

<img width="723" height="371" alt="image" src="https://github.com/user-attachments/assets/d3a1a89b-aa9b-40b2-b7cd-9b63bad4cd22" />

### VPC (Virtual Private Cloud)
AWS 내부에서 독립된 네트워크 공간을 구성하는 서비스
CIDR 기반 IP 대역을 생성하고, 이후 생성되는 리소스는 해당 네트워크 범위 내 IP를 할당받는다.

### Subnet
VPC 내부 네트워크를 목적별로 분리한 영역
Public / Private Subnet으로 구분할 수 있으며, Route Table 및 Public IP 연결 여부에 따라 외부 접근 가능 여부가 결정된다.

### Route Table
Subnet 단위의 네트워크 경로 설정 테이블

구성한 Route:

```text
10.0.0.0/24 → local
0.0.0.0/0 → Internet Gateway
```

- local : VPC 내부 리소스 간 통신
- Internet Gateway : 외부 인터넷 통신

이를 통해 외부 요청이 Internet Gateway → EC2로 전달될 수 있도록 구성했다.
<img width="704" height="252" alt="image" src="https://github.com/user-attachments/assets/f56c7d5d-0d72-4d27-a81c-917516f26b6f" />


### Nginx 설치 및 실행

```bash
sudo apt update
# 패키지 저장소 정보 최신화

sudo apt install nginx -y
# nginx 설치

sudo systemctl start nginx
# nginx 실행

sudo systemctl enable nginx
# 서버 재시작 시 자동 실행 등록
```

---

## 트러블슈팅

### EC2 생성 후 Public IPv4 미할당

증상

EC2 생성 이후 Public IPv4가 존재하지 않았고, 연결 설정에서 탄력적 IP 해제만 표시되었다.

<img width="712" height="140" alt="image" src="https://github.com/user-attachments/assets/73795c60-4bdd-47cf-a65e-52890fc5bc19" />


### 가설 및 검증

1. 탄력적 IP 연결 여부 확인
2. Public Subnet 연결 여부 확인
3. Subnet의 Public IP 자동 할당 설정 여부 확인

### 원인

EC2 생성 시 연결된 Subnet에서 Public IPv4 자동 할당이 비활성화되어 있었다.

### 조치

생성한 Public Subnet의 "퍼블릭 IPv4 자동 할당" 옵션을 활성화했다.

<img width="694" height="186" alt="image" src="https://github.com/user-attachments/assets/91bfb013-c496-4747-a8ce-3ac53fc45d71" />


### 결과

EC2 생성 시 Public IPv4가 정상 할당되었고, 외부 브라우저 및 EC2 Instance Connect 접근이 가능해졌다.

<img width="708" height="434" alt="image" src="https://github.com/user-attachments/assets/d7dc2b8a-e0ea-4b29-9c69-85fc05bba37b" />

이후 nginx 까지 설치 후 
<img width="710" height="235" alt="image" src="https://github.com/user-attachments/assets/9398b2e9-f207-4d72-a4d9-ca94615d7eec" />

자원 정리 후 
- vpc, routing table, internet gateway, subnet 삭제
- ec2 삭제
- 탄력적 ip, ebs 제거 확인
<img width="794" height="303" alt="image" src="https://github.com/user-attachments/assets/9c433f99-f161-420a-b01c-a30e19d7a206" />

