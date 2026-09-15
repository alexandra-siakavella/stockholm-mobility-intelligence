select
    line_designation,
    transport_mode,

    count(*) as observation_count,

    round(
        avg(delay_seconds)::numeric,
        1
    ) as average_delay_seconds,

    round(
        max(delay_seconds)::numeric,
        1
    ) as maximum_delay_seconds,

    round(
        avg(minutes_until_departure)::numeric,
        1
    ) as average_minutes_until_departure,

    sum(
        case
            when is_cancelled
            then 1
            else 0
        end
    ) as cancelled_observations

from departure_features

group by
    line_designation,
    transport_mode
    