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

public class QSevenMapper3 extends Mapper<LongWritable, Text, Text, Text>
{
    private Text path = new Text();
    private Text id = new Text();

    // private String targetid1 = "3577"; // a Seattle airport
    // private String targetid2 = "3797"; // a New York airport

    private List<String> targetid1; // a Seattle airport [should change to a list]
    private List<String> targetid2;

    public void setup(Context context)
    {
        Configuration conf = context.getConfiguration();
        targetid1 = Arrays.asList(conf.get("TargetId1").strip().split("\\s+"));
        targetid2 = Arrays.asList(conf.get("TargetId2").strip().split("\\s+"));
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
        
        // filter for matching paths
        if (targetid1.contains(record[1]) && targetid2.contains(record[record.length - 1]))
        {
            // path to expand
            id.set(record[0]);
            context.write(id, path);
        }
    }
}