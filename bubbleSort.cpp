#include<iostream>
#include<stdio.h>
#include<conio.h>
#define max 10
using namespace std;
int arr[max];
int last = -1;
void insert(){
    if(last == max-1){
        cout<<"Array is full"<<endl;
    }
    else{
        last++;
        cout<<"Enter value : ";
        cin>>arr[last];
    }
}
void swap(int f,int s){
    int c = arr[f];
    arr[f] = arr[s];
    arr[s] = c;
    
}
void bubble_sort(){
    if(last == -1){
        cout<<"Array is empty :"<<endl;
    }
    else{
        int n = last-1;
        for(int i=0;i<=n;i++){
            for(int j=0;j<=n-i;j++){
                if(arr[j]>arr[j+1]){
                    swap(j,j+1);
                }
            }
            
        }
    }

}
void display(){
    if(last == -1){
        cout<<"Array is empty"<<endl;
    }
    else{
        for(int i=0;i<=last;i++){
            cout<<arr[i]<<" ";
        }
    }
    cout<<endl;
}
int main(){
    int ch;
    bool c = true;
    while(c){
        cout<<"1 for insert value \n2 for sorting \n3 for display \n4 for exit"<<endl;
        cout<<"Enter your choice : ";
        cin>>ch;
        switch(ch){
            case 1:{insert();break;}
            case 2:{bubble_sort();break;}
            case 3:{display();break;}
            case 4:{c = false;break;}
            default:{cout<<"You enter wrong option"<<endl;}
        }
    }
    return 0;
}
