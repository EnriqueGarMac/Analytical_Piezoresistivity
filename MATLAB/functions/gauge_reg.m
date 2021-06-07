
function [gauge,linlength1,linlength5]=gauge_reg(x,y)

if x(1)~=0
xtot=[0,x];
ytot=[0,y];
else
xtot=x;
ytot=y; 
end

x=[xtot(1),xtot(2)];
y=[ytot(1),ytot(2)];

p=polyfit(x,y,1);
yfit=polyval(p,x);
yresid=y-yfit;
SSresid=sum(yresid.^2);
SStotal=(length(y)-1)*var(y);
rsq=1-SSresid/SStotal;

rsq_limit=0.9999;
cont=1;
while rsq>rsq_limit && cont+1<=length(xtot)
cont=cont+1;
    
x=xtot(1:cont);
y=ytot(1:cont);

p=polyfit(x,y,1);
yfit=polyval(p,x);
yresid=y-yfit;
SSresid=sum(yresid.^2);
SStotal=(length(y)-1)*var(y);
rsq=1-SSresid/SStotal;
end

p_ref=ytot(cont)./(xtot(cont));



    cont_level=0;
    cont_level2=0;
    length1=xtot(end);
    length5=xtot(end);
for i=cont:length(xtot)

    if abs(1-ytot(i)/(xtot(i)*p_ref))>0.05 && cont_level==0
    length5=xtot(i);
    cont_level=1;
    end
    if abs(1-ytot(i)/(xtot(i)*p_ref))>0.01 && cont_level2==0
    length1=xtot(i);
    cont_level2=1;
    end

end


% Store variables

gauge=p_ref;
linlength1=length1;
linlength5=length5;
end