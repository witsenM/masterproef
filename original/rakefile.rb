class Time
    attr_accessor(:year, :month, :day, :hour, :min)

    def initialize(year, month, day, hour, min)
        @year, @month, @day, @hour, @min = year, month, day, hour, min
    end

    def ==(other)
        @year == other.year && @month == other.month && @day == other.day && @hour == other.hour && @min == other.min
    end

    def next()
        @min += 1
        if @min >= 60
            @min = 0
            @hour += 1
            if @hour == 24
                @day += 1
                @hour = 0
            end
        end
    end

end

task :remove do
    fps = FileList.new("small*.jpg").sort()
    puts fps

    re = /small-([\d]*)-([\d]*)-([\d]*)-([\d]*)-([\d]*).jpg/

    to_remove = []

    prev_fp = nil
    prev_time = nil
    fps.each do |fp|
        puts fp
        if md = re.match(fp)
            year, month, day, hour, min = *md[1..5].map{|e|e.to_i()}
            time = Time.new(year, month, day, hour, min)

            if prev_time
                prev_time.next()
                if time == prev_time
                    to_remove << prev_fp
                end
            end

            prev_time = time
            prev_fp = fp
        end
    end

    to_remove.each do |fp|
        File.delete(fp)
    end
end
