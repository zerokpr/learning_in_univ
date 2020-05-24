#include<pthread.h>

#define TH_MAX 4

int rcount; // 空いているCPUの数
int rcou

struct th_data{
    int req_n; // 必要なCPU数
    pthread_cond_t cvar;
    int isWaiting; // 待ってるかどうか
} tvar[TH_MAX];

int th_waiter_search(void){
    int i;
    for(i = 0; i < TH_MAX; ++i){
        if(tvar[i].req_n < rcount && tvar[i].isWaiting){ // 起こしてよいスレッドを起こす
            return i;
        }
    }
    return -1; // 起こせるスレッドがなかったら-1
}

void get_resource(int reqnum){
    pthread_mutex_lock(&mtx);
    while(rcouut < reqnum){
        pthread_cond_wait(&cvar, &mtx);
    }
    rcount -= reqnum;
    pthread_mutex_unlock(&mtx);
}

void release_resource(){
    pthread_mutex_lock(&mtx);
    int awake_num = th_waiter_search(); // 起こすべき数
    while(awake_num != -1){
        pthread_cond_signal(&cvar[awake_num], &mtx);
        rcount += awake_num+1;
        tvar[awake_num].isWaiting = 0;
        awake_num = th_waiter_search();
    }
    pthread_mutex_unlock(&mtx);
}
