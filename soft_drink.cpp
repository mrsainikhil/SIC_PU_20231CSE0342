#include<iostream>
using namespace std;
int main(){
int n,k,l,c,d,p,nl,np;
cin>>n>>k>>l>>c>>d>>p>>nl>>np;
int volume=k*l;
int drinks=volume/(n*nl);
int lemons=(c*d)/n;
int salt=p/(n*np);
if(drinks<lemons && drinks<salt){
	cout<<drinks<<endl;
}else if(lemons<drinks &&lemons<salt){
	cout<<lemons<<endl;
}else{
	cout<<salt<<endl;
}
return 0;
}