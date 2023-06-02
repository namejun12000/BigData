import org.apache.hadoop.conf.Configured;
import java.nio.file.AccessDeniedException;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Mapper.Context;
import java.io.IOException;

public class QOneMapper extends Mapper<LongWritable, Text, Text, Text>
{
    private Text country = new Text();

    @Override
    protected void map(LongWritable key, Text value, Context context)
        throws IOException, InterruptedException
    {
        String line = value.toString();
        String[] record = line.split(",");
        country.set(record[3]);
        context.write(country, value);
    }
}