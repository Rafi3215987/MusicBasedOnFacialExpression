create database pyconn
use pyconn
create table playlist
(
	emotion varchar(255),
    playlist varchar(255)
);
insert into  playlist(emotion,playlist) values('happy','https://youtube.com/playlist?list=PLW9z2i0xwq0F3-8LieqflLLWLWZQgvhEX&si=l2zUfiF280KThxZ3');
insert into  playlist(emotion,playlist) values('sad','https://youtube.com/playlist?list=PLgzTt0k8mXzHcKebL8d0uYHfawiARhQja&si=dRDBeuPsx-edep6p');
insert into  playlist(emotion,playlist) values('angry','https://youtube.com/playlist?list=PLgzTt0k8mXzHcKebL8d0uYHfawiARhQja&si=dRDBeuPsx-edep6p');
insert into  playlist(emotion,playlist) values('neutral','https://youtube.com/playlist?list=PLP2qAKm-AAm9hIxpLbaMOcG2428lrssd5&si=a_YFmDafFS5oqbkY');
insert into  playlist(emotion,playlist) values('fear','https://youtube.com/playlist?list=PL9urKWGhmkzpypLVBxFxBAaif57vSe8eG&si=O1u1pHKP94nkiUHP');
insert into  playlist(emotion,playlist) values('surprise','https://youtube.com/playlist?list=PL9urKWGhmkzpypLVBxFxBAaif57vSe8eG&si=O1u1pHKP94nkiUHP');
insert into  playlist(emotion,playlist) values('disgust','https://youtube.com/playlist?list=PLS41qcbRSTzvdPNfdVcjf5Uy4kWNiuKIX&si=an38u_tg4VrWeP2e');