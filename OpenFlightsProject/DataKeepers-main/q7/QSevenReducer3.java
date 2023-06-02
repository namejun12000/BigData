import org.apache.hadoop.conf.Configured;

import java.io.IOException;
import java.nio.file.AccessDeniedException;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Reducer.Context;
import java.util.Iterator;

public class QSevenReducer3 extends Reducer<Text, Text, Text, Text>
{
    private Text empty = new Text();
    @Override
    public void reduce(Text key, Iterable<Text> values, Context context)
        throws IOException, InterruptedException
    {
        empty.set("");
        Iterator<org.apache.hadoop.io.Text> valuesIt = values.iterator();
        while (valuesIt.hasNext())
        {
            context.write(empty, valuesIt.next());
        }
    }
}