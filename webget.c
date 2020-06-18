// server side's program test
#include<arpa/inet.h>
#include<unistd.h>
#include<string.h>
#include<stdio.h>
#include<errno.h>
#include<stdlib.h>

// prototype declaration
void strshift(char* buff);
void file_output(FILE* ostream, FILE* inputfile);

// socket情報
struct sockaddr_in serv_addr;

int main(){
  char buff[256];

  // socketを作る
  int sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if(sockfd < 0){
    perror("socket error:");
    return 0;
  }

  // addressを作る
  memset(&serv_addr, 0, sizeof(struct sockaddr_in));
  serv_addr.sin_family = AF_INET;
  serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
  serv_addr.sin_port = htons(80); // portnum

  // socketにaddressを割り当てる
  if(bind(sockfd, (struct sockaddr *)&serv_addr, sizeof(struct sockaddr_in)) < 0){
    perror("bind error:");
    return 0;
  }

  // connection要求を待ちはじめるよう指示
  if(listen(sockfd, 5) < 0){
    perror("listen error:");
    return 0;
  }
  
  FILE *istream;
  FILE *file;
  int new_sockfd;

  int isFirst = 1;
  char mode[10], fileName[50], httpVer[10]; 
  
  while(1){
    // 要求があったらそれを受け付ける（なければ待つ）
    new_sockfd = accept(sockfd, NULL, NULL);
    if(new_sockfd < 0){
      perror("accept error:");
      return 0;
    }
    istream = fdopen(new_sockfd, "r+");
    if(istream == 0){
      perror("fdopen error:");
      return 0;
    }

    // load request
    while(1){
      if(fgets(buff, 1024, istream) == 0) break;
      if(isFirst){
	isFirst = 0;
	sscanf(buff, "%s %s %s", mode, fileName, httpVer);
      }
      printf("%s", buff);
      if(buff[0] == '\r' && buff[1] == '\n') break;
    }
    isFirst = 1;

    printf("fileName is %s\n", fileName);
    strshift(fileName); // shift string front
    printf("fileName has changed: %s\n", fileName);

    file = fopen(fileName, "r");
    if(file == 0){
      perror("file open error:");
      return 0;
    }
    file_output(istream, file);
    if(fclose(file) != 0){
      perror("fclose error:");
      return 0;
    }

    // 1秒待ってsocketを終了する
    sleep(1);
    if(fclose(istream) != 0){
      perror("fclose error2:");
      return 0;
    }
  }
  
  if(close(sockfd) < 0){
    perror("close error:");
    return 0;
  } 
  return 0;
}

void strshift(char *buff){
  if(*buff == '\0'){
    printf("strshift error: is not string/\n");
    return ;
  }
  int i = 0;
  while(1){
    if( i > 1024){
      printf("strshift error: str may not have null.\n");
      break;
    }
    buff[i] = buff[i+1];
    if(buff[i] == '\0') break;
    ++i;
  }
}

//
void file_output(FILE *ostream, FILE *inputfile){
  char buff[1024];
  char *p;
  while(1){
    if(fgets(buff, 1024, inputfile) == 0) break;
    p = strchr(buff, '\n');
    if(p != 0) *p = '\0';
    if(fprintf(ostream, "%s\r\n", buff) < 0){
      printf("response fprintf error\n");
      exit(1);
    }
  }
}
