import org.apache.hadoop.conf.Configured;

import java.io.IOException;
import java.nio.file.AccessDeniedException;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Reducer.Context;
import java.util.Iterator;

public class QSevenReducer1 extends Reducer<Text, Text, Text, Text>  
{
    @Override
    public void reduce(Text key, Iterable<Text> values, Context context)
        throws IOException, InterruptedException
    {
        Iterator<org.apache.hadoop.io.Text> valuesIt = values.iterator();
        while (valuesIt.hasNext())
        {
            context.write(key, valuesIt.next());
        }
    }
}