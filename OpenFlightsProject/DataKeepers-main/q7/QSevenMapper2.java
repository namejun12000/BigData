import org.apache.hadoop.conf.Configured;
import java.nio.file.AccessDeniedException;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Mapper.Context;
import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class QSevenMapper2 extends Mapper<LongWritable, Text, Text, Text>
{
    private Text path = new Text();
    private Text id = new Text();

    private List<String> targetid1; // a Seattle airport [should change to a list]

    public void setup(Context context)
    {
        Configuration conf = context.getConfiguration();
        targetid1 = Arrays.asList(conf.get("TargetId1").strip().split("\\s+"));
    }

    @Override
    protected void map(LongWritable key, Text value, Context context)
        throws IOException, InterruptedException
    {
        String line = value.toString();
        String[] record = line.split("\\s+");
        String format = "";
        for (int i = 1; i < record.length; i++)
        {
            format = format + record[i] + " ";
        }
        format = format.trim(); // remove trailing space
        path.set(format);

        if (targetid1.contains(record[1]))
        {
            // path to expand
            id.set(record[record.length - 1]);
        }
        else
        {
            // an adjacency path
            id.set(record[1]);
        }

        context.write(id, path);
    }
}