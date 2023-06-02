import org.apache.hadoop.conf.Configured;
import java.nio.file.AccessDeniedException;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Mapper.Context;
import java.io.IOException;

public class QSevenMapper1 extends Mapper<LongWritable, Text, Text, Text>
{
    private Text val = new Text();
    private Text k = new Text();

    @Override
    protected void map(LongWritable key, Text value, Context context)
        throws IOException, InterruptedException
    {
        String line = value.toString();
        String[] record = line.split(",");
        if (record[3].equals("SourceAirportID") == false && record[1].equals("N/A") == false && record[3].equals("N/A") == false && record[5].equals("N/A") == false)
        {
            String path = record[3] + " " + record[1] + " " + record[5];
            val.set(path);
            k.set(key.toString());
            context.write(k, val);
        }
    }
}