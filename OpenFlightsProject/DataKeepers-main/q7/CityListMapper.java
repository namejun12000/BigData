import org.apache.hadoop.conf.Configured;
import java.nio.file.AccessDeniedException;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Mapper.Context;
import java.io.IOException;
import org.apache.hadoop.conf.Configuration;

public class CityListMapper extends Mapper<LongWritable, Text, Text, Text>
{
    private Text k = new Text();
    private Text v = new Text();
    private String targetCity1;
    private String targetCity2;

    public void setup(Context context)
    {
        Configuration conf = context.getConfiguration();
        targetCity1 = conf.get("TargetCity1");
        targetCity2 = conf.get("TargetCity2");
    }

    @Override
    protected void map(LongWritable key, Text value, Context context)
        throws IOException, InterruptedException
    {
        String line = value.toString();
        line = line.strip();
        String[] record = line.split(",");

        if (record[2].equals(targetCity1))
        {
            k.set(targetCity1);
            v.set(record[0]);
            context.write(k, v);
        }
        else if (record[2].equals(targetCity2))
        {
            k.set(targetCity2);
            v.set(record[0]);
            context.write(k, v);
        }
    }
}