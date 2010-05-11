create table plays (
    play_id integer primary key autoincrement,
    played_at datetime not null,
    song_id integer,
    foreign key(song_id) references songs (song_id)
);

create table artists (
    artist_id integer primary key autoincrement,
    name text
);

create table songs (
    song_id integer primary key autoincrement,
    name text,
    artist_id integer,
    foreign key(artist_id) references artists (artist_id)
);
