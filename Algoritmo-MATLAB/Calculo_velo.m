%clear
clc



    H=input('Altura luminarias: H=');
    S=input('Distancia entre luminarias: S='); 
    Wl=input('Ancho del camino < 30m: W='); 
    Lanes=input('Número de carriles: ');
    Nc=Lanes*3;
    Rot=input('¿Rotación de 90 grados? Si(1)/No(0): ');
    Fm=input('Factor de Mantenimiento: ');
    Age=23; %edad del conductor
    Ohang=input('Saliente sobre la calzada: T=');
    Distri=input('Distribución: Single-side-Right(0)/Single-side-Left(1)/Double-side(2)/Double-side-staggered(3) : ');
    
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
Nlum=Nlumback+Nlumfor+1;

if Distri==0
    ni=1;
    for ni=ni:Nlum   
        Lx(ni)=S*-(Nlumback+1-ni);
        %[-3S,-2S,-S,0,S,2S];
        Ly(ni)=0+Ohang;   
    end
elseif Distri==1
        ni=1;
    for ni=ni:Nlum   
        Lx(ni)=S*-(Nlumback+1-ni);
        Ly(ni)=Wl-Ohang;   
    end
elseif Distri==2
        ni=1;
    for ni=ni:Nlum  
        Lx(ni)=S*-(Nlumback+1-ni);
        Lx(ni+Nlum)=S*-(Nlumback+1-ni);
        Ly(ni)=0+Ohang;
        Ly(ni+Nlum)=Wl-Ohang; 
    end
    Nlum=Nlum*2;
elseif Distri==3
        ni=1;
    for ni=ni:Nlum
        Lx(ni)=S*-(Nlumback+1-ni);
        Lx(ni+Nlum)=S*-(Nlumback+1-ni)+S*0.5;
        Ly(ni)=0+Ohang;
        Ly(ni+Nlum)=Wl-Ohang; 
    end
    Nlum=Nlum*2;
   
    
end



%Arreglo coordenada x y arreglo y


ni=1;

for ni=ni:Nlum
    i=1;
for i=i:Nc
    j=1;
for j=j:N
    if Px(i,j)-Lx(ni)==0 && Py(i,j)-Ly(ni)==0
        CeL(i,j,ni)=0
    elseif Px(i,j)-Lx(ni)>0 && Py(i,j)-Ly(ni)>=0
        CeL(i,j,ni)=atan((Py(i,j)-Ly(ni))/(Px(i,j)-Lx(ni)))*180/pi;
    elseif Px(i,j)-Lx(ni)==0 && Py(i,j)-Ly(ni)>=0
        CeL(i,j,ni)=90
    elseif Px(i,j)-Lx(ni)<0 && Py(i,j)-Ly(ni)>=0
        CeL(i,j,ni)=atan((Py(i,j)-Ly(ni))/(Px(i,j)-Lx(ni)))*180/pi+180;
    elseif Px(i,j)-Lx(ni)<0 && Py(i,j)-Ly(ni)<=0
        CeL(i,j,ni)=atan((Py(i,j)-Ly(ni))/(Px(i,j)-Lx(ni)))*180/pi+180;
    elseif Px(i,j)-Lx(ni)==0 && Py(i,j)-Ly(ni)<=0
        CeL(i,j,ni)=90
    elseif Px(i,j)-Lx(ni)>0 && Py(i,j)-Ly(ni)<=0
        CeL(i,j,ni)=atan((Py(i,j)-Ly(ni))/(Px(i,j)-Lx(ni)))*180/pi+360;
    end
    GammaL(i,j,ni)=atan((sqrt((Px(i,j)-Lx(ni))^2+(Py(i,j)-Ly(ni))^2)/H))*180/pi;
    
end
end 
end
%%Rotación Iluminarias superiores

if Distri==1
    ni=1
    for ni=ni:Nlum
    i=1;
    for i=i:Nc
    j=1;
    for j=j:N
    
        CeL(i,j,ni)=CeL(i,j,ni)+180;
        if CeL(i,j,ni)>=360
            CeL(i,j,ni)=CeL(i,j,ni)-360;
        end
        
    end
    end
    end
    
end
if Distri==2 || Distri==3
    ni=Nlum/2+1
    for ni=ni:Nlum
    i=1;
    for i=i:Nc
    j=1;
    for j=j:N
    
        CeL(i,j,ni)=CeL(i,j,ni)+180;
        if CeL(i,j,ni)>=360
            CeL(i,j,ni)=CeL(i,j,ni)-360;
        end
        
    end
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
Eav=mean(Illuminance);
Eav=mean(Eav)


Emax=max(Illuminance);
Emax=max(Emax)
Emin=min(Illuminance);
Emin=min(Emin)
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



no=1;
for no=no:Lanes
    ni=1;
for ni=ni:Nlum
    i=1;
for i=i:Nc
    j=1;
for j=j:N
    u=[Lx(ni)-Px(i,j),-Ly(ni)+Py(i,j)];
    u=u/norm(u);
    v=[-(Ox(no)-Px(i,j)),Oy(no)-Py(i,j)];
    v=v/norm(v);
    Beta(i,j,ni,no)=(180/pi)*acos(dot(v,u)/(norm(u)*norm(v)));
    
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
        B(i,j,ni,no)=19;
        
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

no=1;
for no=no:Lanes
    Lavbar(no)=Lav(1,1,no);    
end
%gl1=Lmin/Lav
%gl2=Lmin/Lmax
%gl3=Lav/Lmax

%% CALCULO DE TI 
%Se debe incluir A=23 (23 años conductor) al inicio





%% EK
Lx=0;
Ly=0;
no=1
for no=no:Lanes
    if H>2
        Ox(no)=-2.75*(H-1.5);    
    end
end
Nlumback=floor(0*H/S);
Nlumfor=floor(12*H/S)+1;
Nlum=Nlumback+Nlumfor+1;

if Distri==0
    ni=1;
    for ni=ni:Nlum   
        Lx(ni)=S*-(Nlumback+1-ni);
        %[-3S,-2S,-S,0,S,2S];
        Ly(ni)=0+Ohang;   
    end
elseif Distri==1
        ni=1;
    for ni=ni:Nlum   
        Lx(ni)=S*-(Nlumback+1-ni);
        Ly(ni)=Wl-Ohang;   
    end
elseif Distri==2
        ni=1;
    for ni=ni:Nlum  
        Lx(ni)=S*-(Nlumback+1-ni);
        Lx(ni+Nlum)=S*-(Nlumback+1-ni);
        Ly(ni)=0+Ohang;
        Ly(ni+Nlum)=Wl-Ohang; 
    end
    Nlum=Nlum*2;
elseif Distri==3
        ni=1;
    for ni=ni:Nlum
        Lx(ni)=S*-(Nlumback+1-ni);
        Lx(ni+Nlum)=S*-(Nlumback+1-ni)+S*0.5;
        Ly(ni)=0+Ohang;
        Ly(ni+Nlum)=Wl-Ohang; 
    end
    Nlum=Nlum*2;
   
    
end



%Arreglo coordenada x y arreglo y

ni=1;
for ni=ni:Nlum
    no=1;
for no=no:Lanes
    if Ox(no)-Lx(ni)==0 && Oy(no)-Ly(ni)==0
        CeL(no,ni)=0
    elseif Ox(no)-Lx(ni)>0 && Oy(i,j)-Ly(ni)>=0
        CeL(no,ni)=atan((Oy(no)-Ly(ni))/(Ox(no)-Lx(ni)))*180/pi;
    elseif Ox(no)-Lx(ni)==0 && Oy(no)-Ly(ni)>=0
        CeL(no,ni)=90
    elseif Ox(no)-Lx(ni)<0 && Oy(no)-Ly(ni)>=0
        CeL(no,ni)=atan((Oy(no)-Ly(ni))/(Ox(no)-Lx(ni)))*180/pi+180;
    elseif Ox(no)-Lx(ni)<0 && Oy(no)-Ly(ni)<=0
        CeL(no,ni)=atan((Oy(no)-Ly(ni))/(Ox(no)-Lx(ni)))*180/pi+180;
    elseif Ox(no)-Lx(ni)==0 && Oy(no)-Ly(ni)<=0
        CeL(no,ni)=90
    elseif Ox(no)-Lx(ni)>0 && Oy(no)-Ly(ni)<=0
        CeL(no,ni)=atan((Oy(no)-Ly(ni))/(Ox(no)-Lx(ni)))*180/pi+360;
    end
    GammaL(no,ni)=atan((sqrt((Ox(no)-Lx(ni))^2+(Oy(no)-Ly(ni))^2)/H))*180/pi+1;
    
end
end 

%%Rotación Iluminarias superiores
if Distri==2 || Distri==3
    ni=Nlum/2+1
    for ni=ni:Nlum
    no=1;
    for no=no:Lanes
        CeL(no,ni)=CeL(no,ni)+180;
        if CeL(no,ni)>=360
            CeL(no,ni)=CeL(no,ni)-360;
        end
        
    end
    end
end


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
    no=1;
for no=no:Lanes
    eq3(no)=IES(yfL(no,nl),CfL(no,nl))+((CL(no,nl)-CfL(no,nl))/(CcL(no,nl)-CfL(no,nl)))*(IES(yfL(no,nl),CcL(no,nl))-IES(yfL(no,nl),CfL(no,nl)));
    eq4(no)=IES(ycL(no,nl),CfL(no,nl))+((CL(no,nl)-CfL(no,nl))/(CcL(no,nl)-CfL(no,nl)))*(IES(ycL(no,nl),CcL(no,nl))-IES(ycL(no,nl),CfL(no,nl)));
    IL(no,nl)=eq3(no)+((yL(no,nl)-yfL(no,nl))/(ycL(no,nl)-yfL(no,nl)))*(eq4(no)-eq3(no));
end
end 






    nl=1;
    for nl=nl:Nlum
    no=1;
    for no=no:Lanes


            Ek(no,nl)=(IL(no,nl)*((cos(GammaL(no,nl)*pi/180))^2)*sin(GammaL(no,nl)*pi/180))/(H-1.5)^2;
    end
    end
    

     
        
       

Ek







%%
nl=1; %Indice Luminaria
no=1; %Indice observador
for no=no:Lanes
    nl=1;
    for nl=nl:Nlum
        thetak(no,nl)=(180/pi)*acos(((Lx(nl)-Ox(no))*cos(1*pi/180)+ (H-Oz(no))*sin(-1*pi/180))/(sqrt((Lx(nl)-Ox(no))^2+(Ly(nl)-Oy(no))^2+(H-Oz(no))^2)));
    end
end    

no=1;
for no=no:Lanes
    LV(no)=0;
end

no=1;
for no=no:Lanes
    nl=1;
    for nl=nl:Nlum
        if thetak(no,nl)<=60 && 1.5<thetak(no,nl)
        LV(no)=LV(no)+9.86*(1+(Age/66.4).^4)*Ek(nl)/(thetak(no,nl).^2);
        elseif thetak(no,nl)<=1.5 && 0.1<thetak(no,nl)
        LV(no)=LV(no)+5*((1+(Age/62.5).^4))*Ek(nl)/(thetak(no,nl).^2)+10*Ek(nl)/(thetak(no,nl).^3);
        end
    end
end
% Lavbar=[1.14,1.20,..] % Promedio de Luminancia por observador  

no=1;
for no=no:Lanes
    if Lavbar(no)<=5
    fTI(no)=65*LV(no)/(0.8*Lavbar(no));
    end
    if Lavbar(no) >5
    fTI(no)=95*LV(no)/(1.05*Lavbar(no));
    end
end
    
fTI
