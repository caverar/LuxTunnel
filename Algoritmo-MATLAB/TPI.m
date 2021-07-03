%clear
clc



    H=input('Altura luminarias: H=');
    S=input('Distancia entre luminarias: S='); 
    Wl=input('Ancho del camino < 30m: W='); 
    Lanes=input('Número de carriles: ');
    Nc=Lanes*3;
    Rot=input('¿Rotación de 90 grados? Si(1)/No(0): ');
    Fm=0.5;

%Nlum=input('Número de luminarias: ');

%% Puntos de calculo en la malla
if S<=30
    N=10;
    D=S/N;
else 
    N=11;
    D=S/N;
    while D>3
        N=N+1;
        D=S/N;
    end
end


nl=1;   %Contador para los carriles
for nl=nl:Nc
Px(nl,1)=D/2;
end
ni=1;
nj=1;
for ni=ni:Nc
    nj=1;
for nj=nj:N-1
    Px(ni,nj+1)=Px(1,nj)+D;
end
end 

ni=1;
nj=1;
de=Wl/(Nc);
nl=1;
for nl=nl:Nc
Py(nl,1)=[de*(0.5+1*(nl-1))];
end

nl=1;
nj=1;
for nj=nj:N-1
nl=1;
for nl=nl:Nc

    Py(nl,nj+1)=Py(nl,nj);
end
end
%% Coordenadas Gamma y C

Nlumback=floor(5*H/S);
Nlumfor=floor(12*H/S)+1;
ni=1;
Nlum=Nlumback+Nlumfor+1;
for ni=ni:Nlum
    
Lx(ni)=S*-(Nlumback+1-ni);
%[-3S,-2S,-S,0,S,2S];
Ly(ni)=0;
end
%Arreglo coordenada x y arreglo y


ni=1;
for ni=ni:Nlumback+1
    i=1;
for i=i:Nc
    j=1;
for j=j:N
    CeL(i,j,ni)=atan((Py(i,j)-Ly(ni))/(Px(i,j)-Lx(ni)))*180/pi;
    GammaL(i,j,ni)=atan((sqrt((Px(i,j)-Lx(ni))^2+(Py(i,j)-Ly(ni))^2)/H))*180/pi;
end
end 
end

ni=ni+1;
for ni=ni:Nlum
    i=1;
for i=i:Nc
    j=1;
for j=j:N
    CeL(i,j,ni)=180+atan((Py(i,j)-Ly(ni))/(Px(i,j)-Lx(ni)))*180/pi;
    GammaL(i,j,ni)=atan((sqrt((Px(i,j)-Lx(ni))^2+(Py(i,j)-Ly(ni))^2)/H))*180/pi;
end
end 
end


%%

%Leer archivo .IES
%Crear el arreglo de puntos de medición
%La matriz de coordenadas de la fotometria

%I(C,y)

A=importdata('proof.txt');
Stepgamma=5;
StepC=10;
Indexgamma=180/5+1;
IndexC=360/10+1;
sizem=size(A);
i=1;
j=1;
x=1;
y=1;

%%
while x<=sizem(1)
if isnan(A(x,y))==0
    for x = x:sizem(1)
    
        for y=1:sizem(2)
            if isnan(A(x,y))==1
        break
        end  
            IES(i,j)=A(x,y);
            i=i+1;
             
        end
                  
    if isnan(A(x,y))==1
            break
            end
 
    end
else
    x=x+1;
    j=j+1;
    y=1;
    i=1;
end
end    
%% 
if Rot==1
t=29;
for t=t:36;
    IESbu(:,t-28)=IES(:,t);
end    
r=1;
for r=r:28
    IESbu2(:,r)=IES(:,r);       
end
r=1;
for r=r:28
    IES(:,r+9)=IESbu2(:,r);       
end
IES(:,1)=IES(:,37);
t=2;
for t=t:9
    IES(:,t)=IESbu(:,t-1);
end
end


CL=CeL/StepC;
CL=CL+1;



CfL=floor(CL);
CcL=ceil(CL);

yL=GammaL/Stepgamma;
yL=yL+1;
yfL=floor(yL);
ycL=ceil(yL);

%% Iluminancia

nl=1;
for nl=nl:Nlum
    i=1;
for i=i:Nc
    j=1;
for j=j:N
    eq3(i,j)=IES(yfL(i,j,nl),CfL(i,j,nl))+((CL(i,j,nl)-CfL(i,j,nl))/(CcL(i,j,nl)-CfL(i,j,nl)))*(IES(yfL(i,j,nl),CcL(i,j,nl))-IES(yfL(i,j,nl),CfL(i,j,nl)));
    eq4(i,j)=IES(ycL(i,j,nl),CfL(i,j,nl))+((CL(i,j,nl)-CfL(i,j,nl))/(CcL(i,j,nl)-CfL(i,j,nl)))*(IES(ycL(i,j,nl),CcL(i,j,nl))-IES(ycL(i,j,nl),CfL(i,j,nl)));
    IL(i,j,nl)=eq3(i,j)+((yL(i,j,nl)-yfL(i,j,nl))/(ycL(i,j,nl)-yfL(i,j,nl)))*(eq4(i,j)-eq3(i,j));
end
end 
end



i=1;
for i=i:Nc
    j=1;
for j=j:N
    nl=1;
    for nl=nl:Nlum
        Illuminance(i,j)=0;
    end
end
end 

i=1;
for i=i:Nc
    j=1;
for j=j:N
    nl=1;
    for nl=nl:Nlum
        Illuminance(i,j)=Illuminance(i,j)+(IL(i,j,nl)*((cos(GammaL(i,j,nl)*pi/180))^3));
    end
end
end 
Illuminance=Illuminance*Fm/H^2
Emax=max(Illuminance);
Emax=max(Emax)
Emin=min(Illuminance);
Emin=min(Emin)
Eav=mean(Illuminance);
Eav=mean(Eav)
g1=Emin/Eav
g2=Emin/Emax
g3=Eav/Emax




%% Observer
ni=1;
for ni=ni:Lanes
    
    Ox(ni)=-60;
    Oy(ni)=Py(2+3*(ni-1));
    Oz(ni)=1.5;
end

%C en grados
no=1;
for no=no:Lanes
    ni=1;
for ni=ni:Nlumback+1
    i=1;
for i=i:Nc
    j=1;
for j=j:N
    if Py(i,j)==Oy(no)
    Beta(i,j,ni,no)=+180-CeL(i,j,ni);
    elseif Py(i,j)<Oy(no)
    Beta(i,j,ni,no)=180-(atan((Oy(no)-Py(i,j))/(Px(i,j)-Ox(no)))*180/pi)-CeL(i,j,ni);
    else
    Beta(i,j,ni,no)=180-(45-(atan((Py(i,j)-Oy(no))/(Px(i,j)-Ox(no)))*180/pi))-(CeL(i,j,ni)-45);
    end
end
end 
end

ni=ni+1;
for ni=ni:Nlum
    i=1;
for i=i:Nc
    j=1;
for j=j:N
    if Py(i,j)==Oy(no)
    Beta(i,j,ni,no)=180-CeL(i,j,ni);
    elseif Py(i,j)<Oy(no)
        if 180-(atan((Oy(no)-Py(i,j))/(Px(i,j)-Ox(no)))*180/pi)-CeL(i,j,ni)>=0
            Beta(i,j,ni,no)=180-(atan((Oy(no)-Py(i,j))/(Px(i,j)-Ox(no)))*180/pi)-CeL(i,j,ni);
        else
            Beta(i,j,ni,no)=abs(180-(atan((Oy(no)-Py(i,j))/(Px(i,j)-Ox(no)))*180/pi)-CeL(i,j,ni));
            %Beta(i,j,ni,no)=360-(atan((Oy(no)-Py(i,j))/(Px(i,j)-Ox(no)))*180/pi)-CeL(i,j,ni);
        end
    else
    Beta(i,j,ni,no)=180-(180-90-(atan((Py(i,j)-Oy(no))/(Px(i,j)-Ox(no)))*180/pi))-(CeL(i,j,ni)-90);
    end
end
end 
end
end

tanG=tan(GammaL*pi/180);
%%
no=1;
for no=no:Lanes
    ni=1;
for ni=ni:Nlum
    i=1;
for i=i:Nc
    j=1;
for j=j:N
    
    if Beta(i,j,ni,no)<=2
        B(i,j,ni,no)=Beta(i,j,ni,no)/2;
    elseif Beta(i,j,ni,no)<=45
        B(i,j,ni,no)=Beta(i,j,ni,no)/5+1;
    elseif Beta(i,j,ni,no)<180
        B(i,j,ni,no)=Beta(i,j,ni,no)/15+7;
    else 
        B(i,j,ni,no)=19
        
end
end
end
end
end
%% 
    ni=1;
for ni=ni:Nlum
    i=1;
for i=i:Nc
    j=1;
for j=j:N
    
    if tanG(i,j,ni)<=2
        tG(i,j,ni)=tanG(i,j,ni)/0.25;
    elseif tanG(i,j,ni)<=12
        tG(i,j,ni)=tanG(i,j,ni)/0.5+4;
    else 
        tG(i,j,ni)=28;
        
end
end
end
end


B=B+1;



Bf=floor(B);
Bc=ceil(B);


tG=tG+1;
tGf=floor(tG);
tGc=ceil(tG);    
    
    
    
    
    
    
 %% Interpolación Beta
no=1;
for no=no:Lanes
nl=1;
for nl=nl:Nlum
    i=1;
for i=i:Nc
    j=1;
for j=j:N
    eq3(i,j)=R(tGf(i,j,nl),Bf(i,j,nl,no))+((B(i,j,nl,no)-Bf(i,j,nl,no))/(Bc(i,j,nl,no)-Bf(i,j,nl,no)))*(R(tGf(i,j,nl),Bc(i,j,nl,no))-R(tGf(i,j,nl),Bf(i,j,nl,no)));
    eq4(i,j)=R(tGc(i,j,nl),Bf(i,j,nl,no))+((B(i,j,nl,no)-Bf(i,j,nl,no))/(Bc(i,j,nl,no)-Bf(i,j,nl,no)))*(R(tGc(i,j,nl),Bc(i,j,nl,no))-R(tGc(i,j,nl),Bf(i,j,nl,no)));

    R1(i,j,nl,no)=eq3(i,j)+((tG(i,j,nl)-tGf(i,j,nl))/(tGc(i,j,nl)-tGf(i,j,nl)))*(eq4(i,j)-eq3(i,j));
    if isnan(R1(i,j,nl,no))
        R1(i,j,nl,no)=0;
    end
end
end 
end
end



no=1;
for no=no:Lanes
i=1;
for i=i:Nc
    j=1;
for j=j:N
    nl=1;
    for nl=nl:Nlum
        Luminance(i,j,no)=0;
    end
end
end 
end


no=1;
for no=no:Lanes
i=1;
for i=i:Nc
    j=1;
for j=j:N
    nl=1;
    for nl=nl:Nlum
        Luminance(i,j,no)=Luminance(i,j,no)+(IL(i,j,nl)*R1(i,j,nl,no));
    end
end
end 
end

Luminance=Luminance*1e-4*Fm/H^2

Lmax=max(Luminance);
Lmax=max(Lmax)

Lmin=min(Luminance);
Lmin=min(Lmin)

Lav=mean(Luminance);
Lav=mean(Lav)

%gl1=Lmin/Lav
%gl2=Lmin/Lmax
%gl3=Lav/Lmax

    