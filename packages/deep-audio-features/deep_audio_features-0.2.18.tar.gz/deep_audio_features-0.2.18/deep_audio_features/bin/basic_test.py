import argparse
import torch
from torch.utils.data import DataLoader
import sys, os
import pickle
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "../../"))
from deep_audio_features.dataloading.dataloading import FeatureExtractorDataset
from deep_audio_features.models.cnn import load_cnn
from deep_audio_features.models.convAE import load_convAE
from deep_audio_features.lib.training import test
from deep_audio_features.utils.model_editing import drop_layers
import deep_audio_features.bin.config
import numpy


def test_model(modelpath, ifile, layers_dropped=0,
               test_segmentation=False, verbose=True):
    """Loads a model and predicts each classes probability

Arguments:

        modelpath {str} : A path where the model was stored.

        ifile {str} : A path of a given wav file,
                      which will be tested.
        test_segmentation {bool}: If True extracts segment level
                        predictions of a sequence
        verbose {bool}: If True prints the predictions

Returns:

        y_pred {np.array} : An array with the probability of each class
                            that the model predicts.
        posteriors {np.array}: An array containing the unormalized
                            posteriors of each class.

    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # Restore model
    with open(modelpath, "rb") as input_file:
        model_params = pickle.load(input_file)
    if "classes_mapping" in model_params:
        task = "classification"
        model, hop_length, window_length = load_cnn(modelpath)
        class_names = model.classes_mapping
        # Apply layer drop
        model = drop_layers(model, layers_dropped)
    else:
        task = "representation"
        model, hop_length, window_length = load_convAE(modelpath)

    model = model.to(device)
    max_seq_length = model.max_sequence_length

    zero_pad = model.zero_pad
    spec_size = model.spec_size
    fuse = model.fuse

    model.max_sequence_length = max_seq_length

    # Create test set
    test_set = FeatureExtractorDataset(X=[ifile],
                                       # Random class -- does not matter at all
                                       y=[0],
                                       fe_method="MEL_SPECTROGRAM",
                                       oversampling=False,
                                       max_sequence_length=max_seq_length,
                                       zero_pad=zero_pad,
                                       forced_size=spec_size,
                                       fuse=fuse, show_hist=False,
                                       test_segmentation=test_segmentation,
                                       hop_length=hop_length, window_length=window_length)

    # Create test dataloader
    test_loader = DataLoader(dataset=test_set, batch_size=1,
                             num_workers=4, drop_last=False,
                             shuffle=False)

    # Forward a sample
    posteriors, preds, _ = test(model=model, dataloader=test_loader,
                                 cnn=True, task=task,
                                 classifier=True if layers_dropped == 0
                                 else False)
    if verbose:
        if task == "classification":
            if layers_dropped == 0:
                print("--> Unormalized posteriors:\n {}\n".format(posteriors))
                print("--> Predictions:\n {}".format([class_names[yy]
                                                      for yy in preds]))
                # show aggregated posteriors:
                posts = numpy.array(posteriors)
                probs = []
                for w in range(posts.shape[0]): # for each segment:
                    p = numpy.exp(posts[w, :]) / numpy.sum(numpy.exp(posts[w, :]))
                    probs.append(p)
                probs = numpy.array(probs)
                p_aggregated = probs.mean(axis=0)
                for ip in numpy.argsort(p_aggregated)[::-1]:
                    print(f"{class_names[ip]}\t{p_aggregated[ip]:.2f}")
        else:
            print("--> Representations:\n {}\n".format(preds))

    return preds, numpy.array(posteriors)


if __name__ == '__main__':

    # Read arguments -- model
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', required=True,
                        type=str, help='Model')

    parser.add_argument('-i', '--input', required=True,
                        type=str, help='Input file for testing')

    parser.add_argument('-s', '--segmentation', required=False,
                        action='store_true',
                        help='Return segment predictions')

    parser.add_argument('-L', '--layers', required=False, default=0,
                        help='Number of final layers to cut. Default is 0.')
    args = parser.parse_args()

    # Get arguments
    model = args.model
    ifile = args.input
    layers_dropped = int(args.layers)
    segmentation = args.segmentation

    # Test the model
    d, p = test_model(modelpath=model, ifile=ifile,
                      layers_dropped=layers_dropped,
                      test_segmentation=segmentation)
