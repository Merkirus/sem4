from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
from analysis import get_player_data, get_player_stat_dict
import matplotlib.pyplot as plt
import numpy as np


def get_visual(club_name1, club_name2, c, kernel, ucl=False):
    if ucl:
        player_data_man = get_player_data(f'UCL/{club_name1}')
        player_data_real = get_player_data(f'UCL/{club_name2}')
    else:
        player_data_man = get_player_data(club_name1)
        player_data_real = get_player_data(club_name2)

    players_sca_man = get_player_stat_dict('sca', player_data_man)
    players_gca_man = get_player_stat_dict('gca', player_data_man)

    players_sca_real = get_player_stat_dict('sca', player_data_real)
    players_gca_real = get_player_stat_dict('gca', player_data_real)

    sca_man = [value[0] for value in players_sca_man.values()]
    gca_man = [value[0] for value in players_gca_man.values()]

    sca_real = [value[0] for value in players_sca_real.values()]
    gca_real = [value[0] for value in players_gca_real.values()]

    data_man = [list(x) for x in zip(sca_man, gca_man)]
    data_real = [list(x) for x in zip(sca_real, gca_real)]

    data = data_man + data_real

    target = []
    i = 0
    while i < len(data_man):
        target.append(0)
        i += 1

    i = 0
    while i < len(data_real):
        target.append(1)
        i += 1

    data = np.array(data)

    X_train, X_test, Y_train, Y_test = train_test_split(
        data, target, train_size=0.8, shuffle=True)

    clf = svm.SVC(kernel=kernel, C=c, gamma='scale')

    clf.fit(X_train, Y_train)

    Y_pred = clf.predict(X_test)

    plt.figure()
    plt.clf()

    club_names = [club_name1, club_name2]

    scatter = plt.scatter(
        # pyright: ignore
        data[:, 0], data[:, 1], c=target, zorder=10, cmap=plt.cm.Paired, edgecolor='k', s=20
    )

    plt.scatter(
        # pyright: ignore
        X_test[:, 0], X_test[:, 1], s=80, facecolors='none', zorder=10, edgecolor='k'
    )

    plt.axis('tight')
    x_min = data[:, 0].min()
    x_max = data[:, 0].max()
    y_min = data[:, 1].min()
    y_max = data[:, 1].max()

    XX, YY = np.mgrid[x_min:x_max:200j, y_min:y_max:200j]
    Z = clf.decision_function(np.c_[XX.ravel(), YY.ravel()])

    Z = Z.reshape(XX.shape)
    plt.pcolormesh(XX, YY, Z > 0, cmap=plt.cm.Paired)  # pyright: ignore
    plt.contour(
        XX,
        YY,
        Z,
        colors=['k', 'k', 'k'],
        linestyles=['--', '-', '--'],
        levels=[-0.5, 0, 0.5],
    )
    plt.title('Przekształcanie okazji strzeleckich na gole')
    plt.legend(handles=scatter.legend_elements()[0], labels=club_names)
    plt.xlabel('Akcje kreujące sztrzały')
    plt.ylabel('Akcje kreujące bramki')

    print(f'Accuracy: {metrics.accuracy_score(Y_test, Y_pred)}')
    print(f'Precision: {metrics.precision_score(Y_test, Y_pred)}')
    print(f'Recall: {metrics.recall_score(Y_test, Y_pred)}')

    plt.show()


if __name__ == "__main__":
    get_visual('Manchester City', 'Real Madrid', 100.0, 'rbf', ucl=True)
    get_visual('Inter', 'Manchester City', 100000.0, 'rbf')
    get_visual('Manchester City', 'Real Madrid', 100000.0, 'rbf')
