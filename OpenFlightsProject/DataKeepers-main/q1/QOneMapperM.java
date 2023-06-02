import org.apache.hadoop.conf.Configured;
import java.nio.file.AccessDeniedException;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Mapper.Context;
import java.io.IOException;
import org.apache.hadoop.conf.Configuration;

public class QOneMapperM extends Mapper<LongWritable, Text, Text, Text>
{
    private String targetCountry;
    private Text country = new Text();

    public void setup(Context context)
    {
        Configuration conf = context.getConfiguration();
        targetCountry = conf.get("Country");
    }

    @Override
    protected void map(LongWritable key, Text value, Context context)
        throws IOException, InterruptedException
    {
        String line = value.toString();
        String[] record = line.split(",");
        String c = record[3].trim();
        if (c.equals(targetCountry))
        {
            country.set(record[3]);
            context.write(country, value);
        }
    }
}