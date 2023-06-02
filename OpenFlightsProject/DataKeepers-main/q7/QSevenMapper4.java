import org.apache.hadoop.conf.Configured;
import java.nio.file.AccessDeniedException;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Mapper.Context;
import java.io.IOException;
import org.apache.hadoop.conf.Configuration;

public class QSevenMapper4 extends Mapper<LongWritable, Text, Text, Text>
{
    private Text k = new Text();
    private int round;

    public void setup(Context context)
    {
        Configuration conf = context.getConfiguration();
        round = Integer.parseInt(conf.get("round"));
    }

    @Override
    protected void map(LongWritable key, Text value, Context context)
        throws IOException, InterruptedException
    {
        String line = value.toString();
        line = line.strip();

        if (line.contains(","))
        {
            // a record
            String[] record = line.split(",");
            if (record[1].equals("Name") == false)
            {
                // record is not the file header
                k.set(record[0]); // group by ID of record
                context.write(k, value);
            }
        }
        else
        {
            // a path
            String[] path = line.split("\\s+");
            if (round - 1 < path.length)
            {
                k.set(path[round - 1]);
            }
            else
            {
                k.set("translated");
            }
            context.write(k, value);
        }
    }
}