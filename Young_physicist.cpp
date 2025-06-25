#include<iostream>
using namespace std;
int main(){
int sum_x=0,sum_y=0,sum_z=0;
int dim;
cin>>dim;
for(int i=0;i<dim;i++){
	int x,y,z;
	cin>>x>>y>>z;
	sum_x+=x;
	sum_y+=y;
	sum_z+=z;
}
if(sum_x==0  && sum_y==0 &&sum_z==0){
	cout<<"YES"<<endl;
}else{
	cout<<"NO"<<endl;
}
return 0;
}