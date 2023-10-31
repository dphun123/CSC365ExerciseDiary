create table
  public.day (
    id bigint generated by default as identity,
    created_at timestamp with time zone not null default now(),
    day_name text null default ''::text,
    diary_id bigint null,
    constraint Day_pkey primary key (id),
    constraint day_diary_id_fkey foreign key (diary_id) references diary (id) on update cascade on delete cascade
  ) tablespace pg_default;

create table
  public.diary (
    id bigint generated by default as identity,
    created_at timestamp with time zone not null default now(),
    constraint Diary_pkey primary key (id)
  ) tablespace pg_default;

create table
  public.entry (
    id bigint generated by default as identity,
    created_at timestamp with time zone not null default now(),
    day_id bigint null,
    reps integer null,
    goal_reps integer null,
    weight integer null,
    goal_weight integer null,
    comments text null,
    exercise_id bigint null,
    constraint Entry_pkey primary key (id),
    constraint entry_day_id_fkey foreign key (day_id) references day (id) on update cascade on delete cascade,
    constraint entry_exercise_id_fkey foreign key (exercise_id) references exercise (id)
  ) tablespace pg_default;

create table
  public.exercise (
    id bigint generated by default as identity,
    name text not null default ''::text,
    description text null,
    body_part text null,
    constraint Exercise_pkey primary key (id)
  ) tablespace pg_default;


insert into
  "Exercise" (name, description, body_part)
values
  (
    'Bench Press',
    'lying on a bench and pressing weight upward using either a barbell or a pair of dumbbells',
    'Chest'
  )