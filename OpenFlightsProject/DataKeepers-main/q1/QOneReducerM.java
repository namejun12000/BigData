import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.conf.Configuration;
import java.io.IOException;
import java.nio.file.AccessDeniedException;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Reducer.Context;
import java.util.Iterator;

public class QOneReducerM extends Reducer<Text, Text, Text, Text>  
{
    @Override
    public void reduce(Text key, Iterable<Text> values, Context context)
        throws IOException, InterruptedException
    {
        for(Text value : values)
        {
            context.write(key, value);
        }
    }
}